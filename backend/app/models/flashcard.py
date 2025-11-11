"""
Flashcard Model
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class FlashcardBase(BaseModel):
    """Base flashcard model"""
    korean: str
    english: str
    example_korean: str
    example_english: str
    category: str = "basic"
    difficulty: int = 1


class FlashcardCreate(FlashcardBase):
    """Flashcard creation model"""
    pass


class FlashcardInDB(FlashcardBase):
    """Flashcard in database"""
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class FlashcardResponse(FlashcardBase):
    """Flashcard response model"""
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True


class UserProgress(BaseModel):
    """User progress on flashcard"""
    id: str = Field(alias="_id")
    user_id: str
    flashcard_id: str
    known: bool = False
    review_later: bool = False
    times_reviewed: int = 0
    last_reviewed_at: Optional[datetime] = None
    accuracy: float = 0.0

    class Config:
        populate_by_name = True


class ProgressUpdate(BaseModel):
    """Progress update model"""
    flashcard_id: str
    known: Optional[bool] = None
    review_later: Optional[bool] = None
