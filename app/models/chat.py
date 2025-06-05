from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Model representing a message in a chat conversation"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    session_id: uuid.UUID
    role: str  # 'user', 'assistant' only
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {"from_attributes": True}


class ChatSession(BaseModel):
    """Model representing a chat session"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    title: str = "New Chat"
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity_at: datetime = Field(default_factory=datetime.now)

    model_config = {"from_attributes": True}


class ChatHistory(BaseModel):
    """Model representing a chat history with all messages"""
    session: ChatSession
    messages: List[Message]


class MessageCreate(BaseModel):
    """Schema for creating a new message"""
    role: str
    content: str


class ChatSessionCreate(BaseModel):
    """Schema for creating a new chat session"""
    title: str = "New Chat"


class ChatSessionUpdate(BaseModel):
    """Schema for updating a chat session"""
    title: Optional[str] = None
