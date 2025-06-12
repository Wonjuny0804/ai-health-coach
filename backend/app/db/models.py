from datetime import datetime
import uuid
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatSession(BaseModel):
    """Model representing a chat session in the database"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    title: str = "New Chat"
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class Message(BaseModel):
    """Model representing a message in the database"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    session_id: uuid.UUID
    role: str  # user, assistant only
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True
