"""
Leaderboard Models
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class LeaderboardEntry(BaseModel):
    """Leaderboard entry model"""
    rank: int
    user_id: str
    username: str
    profile_picture: str
    total_points: int
    words_learned: int
    study_streak: int
    quizzes_completed: int
    level: str


class UserPoints(BaseModel):
    """User points breakdown"""
    id: str = Field(alias="_id")
    user_id: str
    total_points: int = 0
    points_this_week: int = 0
    points_this_month: int = 0
    flashcard_points: int = 0
    quiz_points: int = 0
    streak_points: int = 0
    achievement_points: int = 0
    last_updated: Optional[str] = None

    class Config:
        populate_by_name = True


class PointsActivity(BaseModel):
    """Points earning activity"""
    activity_type: str  # flashcard, quiz, streak, achievement
    points_earned: int
    description: str


class LeaderboardTimeframe(str, Enum):
    """Timeframe for leaderboard rankings"""
    ALL_TIME = "all_time"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class PointsUpdate(BaseModel):
    """Points update request"""
    points: int
    category: Optional[str] = None  # flashcard, quiz, streak, achievement
    reason: Optional[str] = None
