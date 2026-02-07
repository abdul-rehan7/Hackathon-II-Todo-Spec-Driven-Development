import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from backend.src.models.todo import Todo, TodoCreate
from backend.src.main import app
from backend.src.database.connection import get_session, create_db_and_tables # Import create_db_and_tables

# Setup a test database
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

@pytest.fixture(name="session")
def session_fixture():
    # This should now call create_db_and_tables from connection.py
    SQLModel.metadata.create_all(engine) # Ensure tables are created for the test session
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine) # Clean up after tests

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_todo(client: TestClient):
    todo_data = {"title": "Buy milk", "description": "Get 2% milk", "priority": 2}
    response = client.post("/api/v1/todos/", json=todo_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["description"] == "Get 2% milk"
    assert data["priority"] == 2
    assert "id" in data
    assert "completed" in data

def test_create_todo_invalid_priority(client: TestClient):
    todo_data = {"title": "Invalid Todo", "priority": 0}
    response = client.post("/api/v1/todos/", json=todo_data)
    assert response.status_code == 422 # Unprocessable Entity for validation errors

def test_create_todo_empty_title(client: TestClient):
    todo_data = {"title": "", "description": "Empty title should fail"}
    response = client.post("/api/v1/todos/", json=todo_data)
    assert response.status_code == 422 # Unprocessable Entity for validation errors

def test_read_todos(client: TestClient):
    # Create a few todos first
    client.post("/api/v1/todos/", json={"title": "Todo 1"})
    client.post("/api/v1/todos/", json={"title": "Todo 2", "priority": 3})

    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) >= 2 # Should have at least the two we created
    assert any(todo["title"] == "Todo 1" for todo in todos)
    assert any(todo["title"] == "Todo 2" for todo in todos)

def test_read_todos_with_offset_and_limit(client: TestClient):
    # Create more todos for pagination test
    for i in range(5):
        client.post("/api/v1/todos/", json={"title": f"Paginated Todo {i}"})

    response = client.get("/api/v1/todos/?offset=1&limit=2")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2
    # The actual content depends on the order, but we can check for titles
    assert todos[0]["title"].startswith("Paginated Todo")
    assert todos[1]["title"].startswith("Paginated Todo")

def test_update_todo(client: TestClient):
    # First create a todo
    create_response = client.post("/api/v1/todos/", json={"title": "Todo to Update", "description": "Initial desc"})
    todo_id = create_response.json()["id"]

    # Update some fields
    update_data = {"title": "Updated Todo", "completed": True, "priority": 5}
    response = client.put(f"/api/v1/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Initial desc" # Description should remain unchanged if not provided
    assert data["completed"] is True
    assert data["priority"] == 5
    assert data["id"] == todo_id

    # Verify update with a GET request
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["title"] == "Updated Todo"
    assert get_data["completed"] is True
    assert get_data["priority"] == 5

def test_update_todo_not_found(client: TestClient):
    response = client.put("/api/v1/todos/999", json={"title": "Non Existent"})
    assert response.status_code == 404 # Not Found

def test_update_todo_invalid_priority(client: TestClient):
    create_response = client.post("/api/v1/todos/", json={"title": "Todo to Update Invalid"})
    todo_id = create_response.json()["id"]

    response = client.put(f"/api/v1/todos/{todo_id}", json={"priority": 0})
    assert response.status_code == 422 # Unprocessable Entity for validation errors

def test_delete_todo(client: TestClient):
    # First create a todo
    create_response = client.post("/api/v1/todos/", json={"title": "Todo to Delete"})
    todo_id = create_response.json()["id"]

    # Delete the todo
    response = client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo deleted successfully"}

    # Verify it's deleted by trying to retrieve it
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404 # Not Found

def test_delete_todo_not_found(client: TestClient):
    response = client.delete("/api/v1/todos/999")
    assert response.status_code == 404 # Not Found
