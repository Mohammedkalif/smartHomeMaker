from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    response: str


class AIFoodRequest(BaseModel):
    state: str = Field(min_length=1)
    meal_type: str = Field(pattern="^(breakfast|lunch|dinner|snack)$")
    language: str = Field(default="English", min_length=1)


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    language: Optional[str] = None


class AuthCredentials(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class ReminderCreate(BaseModel):
    food_name: str
    reminder_message: str
    duration_minutes: int = Field(gt=0, le=24 * 60)
    has_timing: bool = True


class ReminderUpdate(BaseModel):
    completed: bool
