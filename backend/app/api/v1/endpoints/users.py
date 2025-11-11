"""
User Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime

from app.models.user import UserResponse, UserUpdate
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(**current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update current user profile"""
    db = get_database()
    users_collection = db.users

    # Prepare update data
    update_data = user_update.dict(exclude_unset=True)
    if not update_data:
        return UserResponse(**current_user)

    update_data["updated_at"] = datetime.utcnow()

    # Update user
    await users_collection.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": update_data}
    )

    # Get updated user
    updated_user = await users_collection.find_one({"_id": ObjectId(current_user["_id"])})
    updated_user["_id"] = str(updated_user["_id"])

    return UserResponse(**updated_user)


@router.get("/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user learning statistics"""
    return {
        "words_learned": current_user.get("words_learned", 0),
        "study_streak": current_user.get("study_streak", 0),
        "daily_goal": current_user.get("daily_goal", 20),
        "achievements": current_user.get("achievements", []),
        "level": current_user.get("level", "Beginner")
    }
