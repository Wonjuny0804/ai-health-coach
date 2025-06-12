from datetime import datetime
from typing import Dict, Any, Optional, List
import uuid
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    """Model representing a user in the application"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    
    model_config = {"from_attributes": True}