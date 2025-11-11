"""
Vocabulary Categories Models
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class Category(BaseModel):
    """Vocabulary category model"""
    id: str = Field(alias="_id")
    name: str
    name_korean: str
    description: str
    icon: str
    color: str
    word_count: int = 0
    difficulty_level: str = "beginner"  # beginner, intermediate, advanced
    is_active: bool = True
    sort_order: int = 0

    class Config:
        populate_by_name = True


class CategoryCreate(BaseModel):
    """Create category request"""
    name: str
    name_korean: str
    description: str
    icon: str = "📚"
    color: str = "#2b6cee"
    difficulty_level: str = "beginner"


class CategoryUpdate(BaseModel):
    """Update category request"""
    name: Optional[str] = None
    name_korean: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    difficulty_level: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class UserCategoryProgress(BaseModel):
    """User's progress in a category"""
    id: str = Field(alias="_id")
    user_id: str
    category_id: str
    words_learned: int = 0
    words_mastered: int = 0
    total_words: int = 0
    completion_percentage: float = 0.0
    last_studied: Optional[str] = None
    study_streak: int = 0

    class Config:
        populate_by_name = True


class CategoryStats(BaseModel):
    """Category statistics"""
    category_id: str
    category_name: str
    total_words: int
    words_learned: int
    words_mastered: int
    completion_percentage: float
    average_accuracy: float
    study_time_minutes: int
    last_studied: Optional[str] = None
