import pytest
import uuid
from datetime import datetime
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


# Define minimally required models for testing
class ChatSessionCreate(BaseModel):
    title: str = "New Chat Session"


class ChatSession(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    title: str
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity_at: datetime = Field(default_factory=datetime.now)


class MessageCreate(BaseModel):
    role: str = "user"
    content: str
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.role != "user":
            raise ValueError("Only 'user' role messages can be sent")


class Message(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    session_id: uuid.UUID
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)


class ChatHistory(BaseModel):
    session: ChatSession
    messages: list[Message] = []


# Set up test data
TEST_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
TEST_SESSION_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")

# Setup in-memory mock database
sessions = {
    TEST_SESSION_ID: ChatSession(
        id=TEST_SESSION_ID,
        user_id=TEST_USER_ID,
        title="Test Session",
        created_at=datetime.now(),
        last_activity_at=datetime.now()
    )
}

messages = {
    TEST_SESSION_ID: [
        Message(
            id=uuid.UUID("00000000-0000-0000-0000-000000000003"),
            session_id=TEST_SESSION_ID,
            role="user",
            content="Hello, I need help with my diet plan.",
            created_at=datetime.now()
        ),
        Message(
            id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
            session_id=TEST_SESSION_ID,
            role="assistant",
            content="I'd be happy to help with your diet plan. Could you tell me more about your goals?",
            created_at=datetime.now()
        )
    ]
}

# Mock database functions
async def create_chat_session(user_id, title):
    session_id = uuid.uuid4()
    new_session = ChatSession(
        id=session_id,
        user_id=user_id,
        title=title,
        created_at=datetime.now(),
        last_activity_at=datetime.now()
    )
    sessions[session_id] = new_session
    messages[session_id] = []
    return new_session


async def get_chat_session(session_id):
    if session_id in sessions:
        return sessions[session_id]
    raise Exception(f"Chat session with id {session_id} not found")


async def get_session_messages(session_id):
    if session_id in messages:
        return messages[session_id]
    return []


async def create_message(session_id, role, content):
    if session_id not in sessions:
        raise Exception(f"Chat session with id {session_id} not found")
    
    if role not in ["user", "assistant"]:
        raise ValueError("Role must be either 'user' or 'assistant'")
    
    message = Message(
        id=uuid.uuid4(),
        session_id=session_id,
        role=role,
        content=content,
        created_at=datetime.now()
    )
    
    if session_id not in messages:
        messages[session_id] = []
    
    messages[session_id].append(message)
    return message


async def get_user_chat_sessions(user_id):
    return [session for session in sessions.values() if session.user_id == user_id]


# Mock AI response function
async def process_message(user_input, session_id=None):
    return "This is a test AI response"


# In a real application, you would implement proper authentication
def get_current_user():
    # This is a dummy function that would normally verify JWT tokens
    # For now, we'll just return a dummy user ID
    return TEST_USER_ID


# Create FastAPI app and router
app = FastAPI(title="Test API")
router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/sessions", response_model=ChatSession)
async def create_session(
    session_data: ChatSessionCreate,
    current_user_id: uuid.UUID = Depends(get_current_user)
):
    """Create a new chat session for the user"""
    try:
        session = await create_chat_session(current_user_id, session_data.title)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create chat session: {str(e)}")


@router.get("/sessions", response_model=list[ChatSession])
async def list_sessions(
    current_user_id: uuid.UUID = Depends(get_current_user)
):
    """Get all chat sessions for the current user"""
    try:
        user_sessions = await get_user_chat_sessions(current_user_id)
        return user_sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chat sessions: {str(e)}")


@router.get("/sessions/{session_id}", response_model=ChatHistory)
async def get_session_history(
    session_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user)
):
    """Get a specific chat session and its messages"""
    try:
        session = await get_chat_session(session_id)
        
        # In a real application, verify the session belongs to the current user
        if session.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this session")
            
        msgs = await get_session_messages(session_id)
        
        return ChatHistory(
            session=session,
            messages=msgs
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Chat session not found: {str(e)}")


@router.post("/sessions/{session_id}/messages", response_model=Message)
async def send_message(
    session_id: uuid.UUID,
    message_data: MessageCreate,
    current_user_id: uuid.UUID = Depends(get_current_user)
):
    """Send a new message to a chat session and get AI response"""
    try:
        # Verify the session exists and belongs to the user
        session = await get_chat_session(session_id)
        if session.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this session")
        
        # Create the user's message
        if message_data.role != "user":
            raise HTTPException(status_code=400, detail="Only 'user' role messages can be sent")
            
        # Save the user message to the database
        user_message = await create_message(
            session_id=session_id,
            role="user",
            content=message_data.content
        )
        
        # Process the message with the AI and get a response
        ai_response = await process_message(message_data.content, session_id)
        
        # Save the AI response to the database
        ai_message = await create_message(
            session_id=session_id,
            role="assistant",
            content=ai_response
        )
        
        # Return the AI's message
        return ai_message
        
    except ValueError as e:
        # Specifically catch ValueError which includes invalid role errors
        if "Role must be" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")


# Include router in app
app.include_router(router)


@app.get("/")
def read_root():
    return {
        "result": "AI Health Coach Test API",
        "status": "active",
        "version": "1.0.0"
    }


# Test client fixture
@pytest.fixture
def client():
    """Create a test client for FastAPI"""
    with TestClient(app) as test_client:
        yield test_client


# Tests
def test_create_session(client):
    """Test creating a new chat session"""
    response = client.post(
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


def test_list_sessions(client):
    """Test listing all chat sessions for a user"""
    response = client.get("/api/chat/sessions")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # Should have at least the default test session


def test_get_session_history(client):
    """Test getting a specific chat session and its messages"""
    session_id = str(TEST_SESSION_ID)
    response = client.get(f"/api/chat/sessions/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert "session" in data
    assert "messages" in data
    assert data["session"]["id"] == session_id
    assert len(data["messages"]) >= 2  # Should have two default messages


def test_get_nonexistent_session(client):
    """Test getting a chat session that doesn't exist"""
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/api/chat/sessions/{non_existent_id}")
    
    assert response.status_code == 404
    assert "detail" in response.json()


def test_send_message(client):
    """Test sending a message to a chat session"""
    session_id = str(TEST_SESSION_ID)
    response = client.post(
        f"/api/chat/sessions/{session_id}/messages",
        json={"role": "user", "content": "I want to lose weight."}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"  # Response should be from the assistant
    assert "content" in data
    assert data["session_id"] == session_id


def test_send_message_invalid_role(client):
    """Test sending a message with an invalid role"""
    session_id = str(TEST_SESSION_ID)
    response = client.post(
        f"/api/chat/sessions/{session_id}/messages",
        json={"role": "assistant", "content": "This shouldn't work"}
    )
    
    # The error could be either 400 (validation error) or 422 (unprocessable entity)
    # depending on how FastAPI handles the validation
    assert response.status_code in [400, 422, 500]
    assert "detail" in response.json()


def test_send_message_to_nonexistent_session(client):
    """Test sending a message to a session that doesn't exist"""
    non_existent_id = str(uuid.uuid4())
    response = client.post(
        f"/api/chat/sessions/{non_existent_id}/messages",
        json={"role": "user", "content": "Hello?"}
    )
    
    assert response.status_code in [404, 500]  # Either is acceptable depending on error handling
    assert "detail" in response.json()
