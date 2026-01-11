"""
Integration tests for complete authentication + Todo workflow
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from backend.src.main import app
from backend.src.database.connection import get_session
from backend.src.models.user import User
from backend.src.models.todo import Todo
from backend.src.services.auth_service import AuthService
from passlib.context import CryptContext
import uuid
from datetime import datetime

# Create test client
client = TestClient(app)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def test_db_session():
    """Create a test database session"""
    from backend.src.database.connection import engine

    # Create tables
    from backend.src.models.user import User
    from backend.src.models.todo import Todo
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

        # Clean up after test
        session.rollback()


def test_complete_auth_and_todo_workflow(test_db_session):
    """Test complete workflow: register -> login -> create todo -> logout"""

    # Step 1: Register a new user
    registration_response = client.post(
        "/api/v1/auth/register",
        data={
            "email": "testuser@example.com",
            "password": "SecurePass123!"
        }
    )

    assert registration_response.status_code == 201, f"Registration failed: {registration_response.text}"

    registration_data = registration_response.json()
    assert "user" in registration_data
    assert "session" in registration_data
    assert registration_data["user"]["email"] == "testuser@example.com"

    # Extract the token from registration
    auth_token = registration_data["session"]["token"]
    assert auth_token is not None

    # Step 2: Verify user was created in database
    user = test_db_session.exec(
        select(User).where(User.email == "testuser@example.com")
    ).first()
    assert user is not None
    assert user.email == "testuser@example.com"

    # Step 3: Use the token to create a todo
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    todo_response = client.post(
        "/api/v1/todos/",
        json={
            "title": "Test todo from auth flow",
            "description": "Created during auth integration test",
            "priority": 1,
            "user_id": str(user.id)  # This should be automatically set by the API
        },
        headers=headers
    )

    # Since the API should set user_id automatically, we might need to adjust the request
    todo_response = client.post(
        "/api/v1/todos/",
        json={
            "title": "Test todo from auth flow",
            "description": "Created during auth integration test",
            "priority": 1
        },
        headers=headers
    )

    assert todo_response.status_code == 201, f"Todo creation failed: {todo_response.text}"

    todo_data = todo_response.json()
    assert todo_data["title"] == "Test todo from auth flow"
    assert todo_data["user_id"] == str(user.id)

    # Step 4: Verify todo was created in database and belongs to user
    todo = test_db_session.get(Todo, todo_data["id"])
    assert todo is not None
    assert todo.user_id == str(user.id)
    assert todo.title == "Test todo from auth flow"

    # Step 5: Get the todo using the same token
    get_todo_response = client.get(
        f"/api/v1/todos/{todo_data['id']}",
        headers=headers
    )

    assert get_todo_response.status_code == 200, f"Get todo failed: {get_todo_response.text}"

    retrieved_todo = get_todo_response.json()
    assert retrieved_todo["id"] == todo_data["id"]
    assert retrieved_todo["title"] == "Test todo from auth flow"

    # Step 6: Get all todos for the user
    get_todos_response = client.get(
        "/api/v1/todos/",
        headers=headers
    )

    assert get_todos_response.status_code == 200, f"Get todos failed: {get_todos_response.text}"

    todos_list = get_todos_response.json()
    assert len(todos_list) >= 1
    assert any(todo["id"] == todo_data["id"] for todo in todos_list)

    # Step 7: Update the todo
    update_response = client.put(
        f"/api/v1/todos/{todo_data['id']}",
        json={
            "title": "Updated test todo",
            "completed": True
        },
        headers=headers
    )

    assert update_response.status_code == 200, f"Update todo failed: {update_response.text}"

    updated_todo = update_response.json()
    assert updated_todo["title"] == "Updated test todo"
    assert updated_todo["completed"] is True

    # Step 8: Try to access the todo with an invalid token (should fail)
    invalid_headers = {
        "Authorization": "Bearer invalid-token",
        "Content-Type": "application/json"
    }

    invalid_access_response = client.get(
        f"/api/v1/todos/{todo_data['id']}",
        headers=invalid_headers
    )

    assert invalid_access_response.status_code == 401, "Invalid token should result in 401 Unauthorized"

    # Step 9: Logout
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers=headers
    )

    assert logout_response.status_code == 200, f"Logout failed: {logout_response.text}"

    logout_data = logout_response.json()
    assert logout_data["message"] == "Successfully logged out"


def test_unauthorized_todo_access():
    """Test that unauthenticated users cannot access todo endpoints"""

    # Try to create a todo without authentication
    todo_response = client.post(
        "/api/v1/todos/",
        json={
            "title": "Unauthorized todo",
            "priority": 1
        }
    )

    assert todo_response.status_code == 401, "Unauthenticated todo creation should fail"

    # Try to get todos without authentication
    get_todos_response = client.get("/api/v1/todos/")

    assert get_todos_response.status_code == 401, "Unauthenticated todo retrieval should fail"


def test_user_isolation():
    """Test that users can only access their own todos"""

    # Create first user
    user1_response = client.post(
        "/api/v1/auth/register",
        data={
            "email": "user1@example.com",
            "password": "SecurePass123!"
        }
    )

    assert user1_response.status_code == 201
    user1_data = user1_response.json()
    user1_token = user1_data["session"]["token"]

    # Create second user
    user2_response = client.post(
        "/api/v1/auth/register",
        data={
            "email": "user2@example.com",
            "password": "SecurePass123!"
        }
    )

    assert user2_response.status_code == 201
    user2_data = user2_response.json()
    user2_token = user2_data["session"]["token"]

    # User 1 creates a todo
    headers1 = {"Authorization": f"Bearer {user1_token}"}
    todo_response = client.post(
        "/api/v1/todos/",
        json={"title": "User 1's todo", "priority": 1},
        headers=headers1
    )

    assert todo_response.status_code == 201
    todo_data = todo_response.json()
    todo_id = todo_data["id"]

    # User 2 should not be able to access User 1's todo
    headers2 = {"Authorization": f"Bearer {user2_token}"}
    access_response = client.get(f"/api/v1/todos/{todo_id}", headers=headers2)

    # Should either get 404 (not found) to prevent enumeration, or 403 (forbidden)
    # The current implementation returns 404 to avoid revealing whether the resource exists
    assert access_response.status_code in [403, 404], f"User isolation failed: {access_response.status_code}"

    # Clean up: logout both users
    client.post("/api/v1/auth/logout", headers=headers1)
    client.post("/api/v1/auth/logout", headers=headers2)


if __name__ == "__main__":
    pytest.main([__file__])