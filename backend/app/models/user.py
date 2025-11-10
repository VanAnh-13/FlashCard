"""
User Model
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    """Base user model"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation model"""
    password: str


class UserLogin(BaseModel):
    """User login model"""
    username_or_email: str
    password: str


class UserInDB(UserBase):
    """User in database"""
    id: str = Field(alias="_id")
    hashed_password: str
    profile_picture: str = "https://lh3.googleusercontent.com/aida-public/AB6AXuC21O5nSDggWM09pPyighOBnT7NHBBfvBB3xi1rzOpkYL3l8VCnbmSHw2oHXf_p1gnbkiFaSywaf6TXAitjIhEtqBd02pI3GynWdxza0SLTMt_sldqLkCNuuNchLXYG72Eddp2yYe_DdS612t_RcY_jtO8_WnyoBNeY9_xW1DQBhDDOaXMSpzDphirEh9TgKYd-ZC6GO7u3yImUlPah_HRtSIp5rS6CpUknNZYSmRQgqpvbPV7kt31uEdgHLYKza9727CNJ0skKqlM"
    level: str = "Beginner"
    daily_goal: int = 20
    words_learned: int = 0
    study_streak: int = 0
    achievements: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class UserResponse(UserBase):
    """User response model"""
    id: str = Field(alias="_id")
    profile_picture: str
    level: str
    daily_goal: int
    words_learned: int
    study_streak: int
    achievements: List[str]

    class Config:
        populate_by_name = True


class UserUpdate(BaseModel):
    """User update model"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    daily_goal: Optional[int] = None
    profile_picture: Optional[str] = None


class Token(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data"""
    user_id: Optional[str] = None
