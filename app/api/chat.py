from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import uuid

from app.db.client import (
    create_chat_session,
    get_chat_session,
    get_session_messages,
    create_message,
    get_user_chat_sessions
)
from app.models.chat import (
    ChatSessionCreate,
    ChatSession,
    MessageCreate,
    Message,
    ChatHistory,
    ChatSessionUpdate
)
from app.core.health_agent import process_message

router = APIRouter(prefix="/api/chat", tags=["chat"])

# In a real application, you would implement proper authentication
def get_current_user():
    # This is a dummy function that would normally verify JWT tokens
    # For now, we'll just return a dummy user ID
    return uuid.UUID("00000000-0000-0000-0000-000000000001")


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
            
        messages = await get_session_messages(session_id)
        
        return ChatHistory(
            session=session,
            messages=messages
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
