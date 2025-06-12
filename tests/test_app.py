from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
from pydantic import BaseModel, Field

# Define self-contained models for testing
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


class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None

app = FastAPI(
    title="AI Health Coach API Test",
    description="Test version of API for the AI Health Coach application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat router
router = APIRouter(prefix="/api/chat", tags=["chat"])

# In a real application, you would implement proper authentication
def get_current_user():
    # This is a dummy function that would normally verify JWT tokens
    # For now, we'll just return a dummy user ID
    return uuid.UUID("00000000-0000-0000-0000-000000000001")

# Mock data
TEST_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
TEST_SESSION_ID = uuid.UUID("00000000-0000-0000-0000-000000000002")

# Mock DB storage
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

# Mock DB functions
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


@router.get("/sessions", response_model=List[ChatSession])
async def list_sessions(
    current_user_id: uuid.UUID = Depends(get_current_user)
):
    """Get all chat sessions for the current user"""
    try:
        sessions = await get_user_chat_sessions(current_user_id)
        return sessions
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

# Include routers
app.include_router(router)

@app.get("/")
def read_root():
    return {
        "result": "AI Health Coach Test API",
        "status": "active",
        "version": "1.0.0"
    }
