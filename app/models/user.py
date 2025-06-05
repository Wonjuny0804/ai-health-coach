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


class UserProfile(BaseModel):
    """Model representing a user's health profile"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    fitness_goals: List[str] = Field(default_factory=list)
    dietary_preferences: List[str] = Field(default_factory=list)
    # health fields removed (health_conditions)
    activity_level: Optional[str] = None  # sedentary, light, moderate, active, very active
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    password: str


class UserProfileCreate(BaseModel):
    """Schema for creating a user profile"""
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    fitness_goals: List[str] = Field(default_factory=list)
    dietary_preferences: List[str] = Field(default_factory=list)
    # health fields removed (health_conditions)
    activity_level: Optional[str] = None


class UserProfileUpdate(BaseModel):
    """Schema for updating a user profile"""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    fitness_goals: Optional[List[str]] = None
    dietary_preferences: Optional[List[str]] = None
    # health fields removed
    activity_level: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
