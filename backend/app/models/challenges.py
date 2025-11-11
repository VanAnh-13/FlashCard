"""
Daily Challenges Models
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class DailyChallenge(BaseModel):
    """Daily challenge model"""
    id: str = Field(alias="_id")
    date: str  # YYYY-MM-DD format
    challenge_type: str  # learn_new_words, complete_quiz, review_flashcards
    target_count: int
    reward_points: int
    description: str
    icon: str

    class Config:
        populate_by_name = True


class UserChallengeProgress(BaseModel):
    """User's progress on daily challenge"""
    id: str = Field(alias="_id")
    user_id: str
    challenge_id: str
    date: str
    current_count: int = 0
    target_count: int
    completed: bool = False
    completed_at: Optional[datetime] = None
    points_earned: int = 0

    class Config:
        populate_by_name = True


class StudySession(BaseModel):
    """Study session tracking"""
    id: str = Field(alias="_id")
    user_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: int = 0
    flashcards_reviewed: int = 0
    quizzes_completed: int = 0
    words_learned: int = 0
    accuracy_rate: float = 0.0
    points_earned: int = 0
    session_type: str = "mixed"  # flashcard, quiz, mixed

    class Config:
        populate_by_name = True


class StudyStreak(BaseModel):
    """Study streak tracking"""
    id: str = Field(alias="_id")
    user_id: str
    current_streak: int = 0
    longest_streak: int = 0
    last_study_date: Optional[str] = None  # YYYY-MM-DD
    study_dates: List[str] = []  # List of study dates

    class Config:
        populate_by_name = True
