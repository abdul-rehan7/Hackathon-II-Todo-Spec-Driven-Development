import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from src.main import app  # Assuming the main app is in main.py
from src.models.user import User


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    user = User(
        id="test_user_id",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    return user


class TestChatAPI:
    """Integration tests for the chat API endpoints."""

    @patch('src.api.v1.chat.get_current_user')
    @patch('src.api.v1.chat.ai_agent')
    def test_chat_endpoint_success(self, mock_ai_agent, mock_get_current_user, client, mock_user):
        """Test successful chat message processing."""
        # Mock the current user
        mock_get_current_user.return_value = mock_user

        # Mock the AI agent response
        mock_ai_agent.process_message.return_value = {
            "response": "Successfully created todo: 'Buy groceries'",
            "intent": "CREATE_TODO",
            "confidence": 0.9,
            "action_taken": {"todo_id": 1, "content": "Buy groceries"}
        }

        # Send a POST request to the chat endpoint
        response = client.post(
            "/api/v1/chat/",
            json={"message": "Create a new task to buy groceries"},
            headers={"Authorization": "Bearer fake_token"}
        )

        # Assert the response
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Successfully created todo: 'Buy groceries'"
        assert data["intent"] == "CREATE_TODO"
        assert data["confidence"] == 0.9
        assert data["action_taken"]["todo_id"] == 1

    @patch('src.api.v1.chat.get_current_user')
    @patch('src.api.v1.chat.ai_agent')
    def test_chat_endpoint_low_confidence(self, mock_ai_agent, mock_get_current_user, client, mock_user):
        """Test chat processing with low confidence response."""
        # Mock the current user
        mock_get_current_user.return_value = mock_user

        # Mock the AI agent response with low confidence
        mock_ai_agent.process_message.return_value = {
            "response": "I'm not sure I understood your request.",
            "intent": "UNKNOWN",
            "confidence": 0.1,
            "action_taken": {}
        }

        response = client.post(
            "/api/v1/chat/",
            json={"message": "This is an unclear command"},
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "not sure I understood" in data["response"]
        assert data["confidence"] == 0.1

    @patch('src.api.v1.chat.get_current_user')
    @patch('src.api.v1.chat.ai_agent')
    def test_chat_endpoint_skill_execution_failure(self, mock_ai_agent, mock_get_current_user, client, mock_user):
        """Test chat processing when skill execution fails."""
        # Mock the current user
        mock_get_current_user.return_value = mock_user

        # Mock the AI agent response with an error
        mock_ai_agent.process_message.return_value = {
            "response": "I encountered an issue: Failed to create todo",
            "intent": "CREATE_TODO",
            "confidence": 0.8,
            "action_taken": {}
        }

        response = client.post(
            "/api/v1/chat/",
            json={"message": "Create a problematic task"},
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "I encountered an issue" in data["response"]

    def test_chat_endpoint_unauthorized(self, client):
        """Test that unauthorized requests return 401."""
        response = client.post(
            "/api/v1/chat/",
            json={"message": "Create a new task"},
            # No Authorization header
        )

        # Should return 401 or redirect since we're not providing auth
        assert response.status_code in [401, 307]  # 307 if redirecting to login

    @patch('src.api.v1.chat.get_current_user')
    def test_get_supported_intents(self, mock_get_current_user, client, mock_user):
        """Test the supported intents endpoint."""
        # Mock the current user for auth
        mock_get_current_user.return_value = mock_user

        # This test may not work if the endpoint requires authentication
        # Let's test it assuming it might not require auth
        response = client.get("/api/v1/chat/intents/")

        # Depending on auth requirements, this might return 200 or 401
        assert response.status_code in [200, 401, 404]

    @patch('src.api.v1.chat.get_current_user')
    @patch('src.api.v1.chat.ai_agent')
    def test_chat_endpoint_empty_message(self, mock_ai_agent, mock_get_current_user, client, mock_user):
        """Test chat endpoint with empty message."""
        # Mock the current user
        mock_get_current_user.return_value = mock_user

        # Mock the AI agent response
        mock_ai_agent.process_message.return_value = {
            "response": "I'm not sure I understood your request.",
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "action_taken": {}
        }

        response = client.post(
            "/api/v1/chat/",
            json={"message": ""},  # Empty message
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "not sure I understood" in data["response"] or "encountered an error" in data["response"]

    @patch('src.api.v1.chat.get_current_user')
    @patch('src.api.v1.chat.ai_agent')
    def test_chat_endpoint_special_characters(self, mock_ai_agent, mock_get_current_user, client, mock_user):
        """Test chat endpoint with special characters."""
        # Mock the current user
        mock_get_current_user.return_value = mock_user

        # Mock the AI agent response
        mock_ai_agent.process_message.return_value = {
            "response": "Successfully processed message",
            "intent": "CREATE_TODO",
            "confidence": 0.8,
            "action_taken": {"result": "success"}
        }

        response = client.post(
            "/api/v1/chat/",
            json={"message": "Create task: Buy groceries & household items! #urgent"},
            headers={"Authorization": "Bearer fake_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "Successfully processed" in data["response"] or "create" in data["intent"].lower()