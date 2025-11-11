"""
Authentication Endpoints
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId

from app.models.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.database import get_database

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    db = get_database()
    users_collection = db.users

    # Check if user exists
    existing_user = await users_collection.find_one({
        "$or": [
            {"email": user_data.email},
            {"username": user_data.username}
        ]
    })

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    # Create user document
    user_dict = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": get_password_hash(user_data.password),
        "profile_picture": "https://lh3.googleusercontent.com/aida-public/AB6AXuC21O5nSDggWM09pPyighOBnT7NHBBfvBB3xi1rzOpkYL3l8VCnbmSHw2oHXf_p1gnbkiFaSywaf6TXAitjIhEtqBd02pI3GynWdxza0SLTMt_sldqLkCNuuNchLXYG72Eddp2yYe_DdS612t_RcY_jtO8_WnyoBNeY9_xW1DQBhDDOaXMSpzDphirEh9TgKYd-ZC6GO7u3yImUlPah_HRtSIp5rS6CpUknNZYSmRQgqpvbPV7kt31uEdgHLYKza9727CNJ0skKqlM",
        "level": "Beginner",
        "daily_goal": 20,
        "words_learned": 0,
        "study_streak": 0,
        "achievements": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = await users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)

    return UserResponse(**user_dict)


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    """Login user and return JWT token"""
    db = get_database()
    users_collection = db.users

    # Find user by username or email
    user = await users_collection.find_one({
        "$or": [
            {"email": login_data.username_or_email},
            {"username": login_data.username_or_email}
        ]
    })

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )

    # Verify password
    if not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )

    # Create access token
    access_token = create_access_token(
        data={"sub": str(user["_id"]), "username": user["username"]}
    )

    return Token(access_token=access_token)
