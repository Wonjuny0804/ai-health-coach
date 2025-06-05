from datetime import datetime, date
from typing import Dict, Any, Optional, List
import uuid
from enum import Enum
from pydantic import BaseModel, Field


class ActivityLevel(str, Enum):
    """Activity level options for user fitness profiles"""
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class HealthData(BaseModel):
    """Model representing user's health tracking data"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    date: date = Field(default_factory=date.today)
    weight_kg: Optional[float] = None
    steps: Optional[int] = None
    calories_consumed: Optional[int] = None
    calories_burned: Optional[int] = None
    water_ml: Optional[int] = None
    sleep_hours: Optional[float] = None
    mood: Optional[str] = None
    stress_level: Optional[int] = None  # 1-10 scale
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class Exercise(BaseModel):
    """Model representing an exercise in a workout plan"""
    name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_minutes: Optional[int] = None
    rest_seconds: Optional[int] = None
    instructions: Optional[str] = None


class WorkoutDay(BaseModel):
    """Model representing a day in a workout plan"""
    day: str  # e.g., "Monday", "Day 1", etc.
    focus: str  # e.g., "Upper Body", "Cardio", "Rest"
    exercises: List[Exercise] = Field(default_factory=list)
    notes: Optional[str] = None


class WorkoutPlan(BaseModel):
    """Model representing a workout plan"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    title: str
    description: Optional[str] = None
    goal: str  # e.g., "Weight Loss", "Muscle Gain"
    difficulty: str  # "Beginner", "Intermediate", "Advanced"
    duration_weeks: int
    frequency_per_week: int
    days: List[WorkoutDay] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class Meal(BaseModel):
    """Model representing a meal in a diet plan"""
    name: str
    foods: List[str]
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fats_g: Optional[float] = None
    notes: Optional[str] = None
    recipe: Optional[str] = None


class DietDay(BaseModel):
    """Model representing a day in a diet plan"""
    day: str  # e.g., "Monday", "Day 1", etc.
    meals: List[Meal] = Field(default_factory=list)
    water_target_ml: Optional[int] = None
    notes: Optional[str] = None


class DietPlan(BaseModel):
    """Model representing a diet plan"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    title: str
    description: Optional[str] = None
    goal: str  # e.g., "Weight Loss", "Maintenance"
    daily_calories: Optional[int] = None
    macros_ratio: Optional[Dict[str, float]] = None  # e.g., {"protein": 0.3, "carbs": 0.4, "fats": 0.3}
    days: List[DietDay] = Field(default_factory=list)
    restrictions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class HealthDataCreate(BaseModel):
    """Schema for creating health tracking data"""
    date: Optional[date] = None
    weight_kg: Optional[float] = None
    steps: Optional[int] = None
    calories_consumed: Optional[int] = None
    calories_burned: Optional[int] = None
    water_ml: Optional[int] = None
    sleep_hours: Optional[float] = None
    mood: Optional[str] = None
    stress_level: Optional[int] = None
    notes: Optional[str] = None


class WorkoutPlanCreate(BaseModel):
    """Schema for creating a workout plan"""
    title: str
    description: Optional[str] = None
    goal: str
    difficulty: str
    duration_weeks: int
    frequency_per_week: int
    days: List[WorkoutDay]


class DietPlanCreate(BaseModel):
    """Schema for creating a diet plan"""
    title: str
    description: Optional[str] = None
    goal: str
    daily_calories: Optional[int] = None
    macros_ratio: Optional[Dict[str, float]] = None
    days: List[DietDay]
    restrictions: List[str] = Field(default_factory=list)
