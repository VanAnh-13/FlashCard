"""
Social Features Models - Friends, Groups, Sharing
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FriendRequest(BaseModel):
    """Friend request model"""
    id: str = Field(alias="_id")
    from_user_id: str
    to_user_id: str
    status: str  # pending, accepted, rejected
    created_at: datetime
    responded_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class Friendship(BaseModel):
    """Friendship model"""
    id: str = Field(alias="_id")
    user1_id: str
    user2_id: str
    created_at: datetime

    class Config:
        populate_by_name = True


class Friend(BaseModel):
    """Friend profile"""
    user_id: str
    username: str
    profile_picture: str
    level: str
    total_points: int
    words_learned: int
    study_streak: int
    is_online: bool = False


class StudyGroup(BaseModel):
    """Study group model"""
    id: str = Field(alias="_id")
    name: str
    description: str
    created_by: str
    members: List[str] = []
    max_members: int = 50
    is_private: bool = False
    created_at: datetime

    class Config:
        populate_by_name = True


class GroupMember(BaseModel):
    """Group member"""
    user_id: str
    username: str
    profile_picture: str
    role: str  # admin, moderator, member
    joined_at: datetime


class Post(BaseModel):
    """Social post/activity"""
    id: str = Field(alias="_id")
    user_id: str
    username: str
    content: str
    post_type: str  # achievement, milestone, study_session, general
    metadata: dict = {}
    likes: List[str] = []
    comments: List[dict] = []
    created_at: datetime

    class Config:
        populate_by_name = True


class ActivityFeed(BaseModel):
    """Activity feed item"""
    id: str
    user_id: str
    username: str
    profile_picture: str
    activity_type: str  # learned_word, completed_quiz, unlocked_achievement, etc.
    description: str
    metadata: dict = {}
    timestamp: datetime


class Challenge(BaseModel):
    """User-to-user challenge"""
    id: str = Field(alias="_id")
    challenger_id: str
    challenged_id: str
    challenge_type: str  # quiz_score, words_learned, study_time
    target_value: int
    duration_days: int
    status: str  # pending, active, completed
    winner_id: Optional[str] = None
    created_at: datetime
    expires_at: datetime

    class Config:
        populate_by_name = True


class ShareableContent(BaseModel):
    """Shareable content"""
    content_type: str  # achievement, progress, streak, score
    title: str
    description: str
    image_url: Optional[str] = None
    share_url: str
