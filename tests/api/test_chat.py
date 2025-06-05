import pytest
import uuid
from fastapi.testclient import TestClient

from app.models.chat import ChatSessionCreate, MessageCreate
from tests.test_app import TEST_SESSION_ID



def test_create_session(test_client):
    """Test creating a new chat session"""
    response = test_client.post(
        "/api/chat/sessions",
        json={"title": "New Test Session"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Test Session"
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data
    assert "last_activity_at" in data


def test_list_sessions(test_client):
    """Test listing all chat sessions for a user"""
    response = test_client.get("/api/chat/sessions")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Our test app should have at least one session by default
    assert len(data) >= 1


def test_get_session_history(test_client):
    """Test getting a specific chat session and its messages"""
    session_id = str(TEST_SESSION_ID)
    response = test_client.get(f"/api/chat/sessions/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert "session" in data
    assert "messages" in data
    assert data["session"]["id"] == session_id
    # Our test app should have messages for this session
    assert len(data["messages"]) >= 2


def test_get_nonexistent_session(test_client):
    """Test getting a chat session that doesn't exist"""
    non_existent_id = str(uuid.uuid4())
    response = test_client.get(f"/api/chat/sessions/{non_existent_id}")
    
    assert response.status_code == 404
    assert "detail" in response.json()


def test_send_message(test_client):
    """Test sending a message to a chat session"""
    session_id = str(TEST_SESSION_ID)
    response = test_client.post(
        f"/api/chat/sessions/{session_id}/messages",
        json={"role": "user", "content": "I want to lose weight."}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"  # Response should be from the assistant
    assert "content" in data
    assert data["session_id"] == session_id


def test_send_message_invalid_role(test_client):
    """Test sending a message with an invalid role"""
    session_id = str(TEST_SESSION_ID)
    response = test_client.post(
        f"/api/chat/sessions/{session_id}/messages",
        json={"role": "assistant", "content": "This shouldn't work"}
    )
    
    # FastAPI returns 422 for Pydantic validation errors
    assert response.status_code in [400, 422]
    assert "detail" in response.json()


def test_send_message_to_nonexistent_session(test_client):
    """Test sending a message to a session that doesn't exist"""
    non_existent_id = str(uuid.uuid4())
    response = test_client.post(
        f"/api/chat/sessions/{non_existent_id}/messages",
        json={"role": "user", "content": "Hello?"}
    )
    
    assert response.status_code in [403, 404, 500]  # Any of these are acceptable depending on error handling
    assert "detail" in response.json()
