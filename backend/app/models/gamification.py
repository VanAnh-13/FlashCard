"""
Gamification Models - Achievements, Badges, and Rewards
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Achievement(BaseModel):
    """Achievement definition"""
    id: str = Field(alias="_id")
    name: str
    description: str
    icon: str
    category: str  # learning, streak, social, mastery
    difficulty: str  # bronze, silver, gold, platinum
    points_reward: int
    requirement_type: str  # words_learned, study_streak, quizzes_completed, etc.
    requirement_value: int
    is_secret: bool = False

    class Config:
        populate_by_name = True


class UserAchievement(BaseModel):
    """User's unlocked achievement"""
    id: str = Field(alias="_id")
    user_id: str
    achievement_id: str
    achievement_name: str
    achievement_icon: str
    unlocked_at: datetime
    points_earned: int

    class Config:
        populate_by_name = True


class Badge(BaseModel):
    """Badge definition"""
    id: str = Field(alias="_id")
    name: str
    description: str
    icon: str
    rarity: str  # common, rare, epic, legendary
    requirement_description: str

    class Config:
        populate_by_name = True


class UserBadge(BaseModel):
    """User's earned badge"""
    id: str = Field(alias="_id")
    user_id: str
    badge_id: str
    badge_name: str
    badge_icon: str
    badge_rarity: str
    earned_at: datetime

    class Config:
        populate_by_name = True


class Reward(BaseModel):
    """Reward for completing milestones"""
    id: str = Field(alias="_id")
    name: str
    description: str
    reward_type: str  # points, badge, title, avatar
    reward_value: str
    icon: str

    class Config:
        populate_by_name = True


class Quest(BaseModel):
    """Quest or mission"""
    id: str = Field(alias="_id")
    name: str
    description: str
    quest_type: str  # daily, weekly, special
    tasks: List[dict]  # List of tasks to complete
    reward_points: int
    reward_badges: List[str] = []
    expires_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        populate_by_name = True


class UserQuest(BaseModel):
    """User's quest progress"""
    id: str = Field(alias="_id")
    user_id: str
    quest_id: str
    quest_name: str
    tasks_progress: List[dict]
    completed: bool = False
    completed_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class Title(BaseModel):
    """User title/rank"""
    id: str = Field(alias="_id")
    name: str
    name_korean: str
    description: str
    requirement_points: int
    color: str
    icon: str

    class Config:
        populate_by_name = True


class AchievementProgress(BaseModel):
    """Progress towards an achievement"""
    achievement_id: str
    achievement_name: str
    achievement_description: str
    achievement_icon: str
    current_value: int
    target_value: int
    progress_percentage: float
    points_reward: int
    unlocked: bool = False
