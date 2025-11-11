"""
Daily Challenges Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, date
from bson import ObjectId
from typing import List
import random

from app.models.challenges import (
    DailyChallenge,
    UserChallengeProgress,
    StudySession,
    StudyStreak
)
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


# Challenge templates
CHALLENGE_TEMPLATES = [
    {
        "challenge_type": "learn_new_words",
        "target_count": 10,
        "reward_points": 50,
        "description": "Learn 10 new Korean words",
        "icon": "📚"
    },
    {
        "challenge_type": "review_flashcards",
        "target_count": 20,
        "reward_points": 30,
        "description": "Review 20 flashcards",
        "icon": "🔄"
    },
    {
        "challenge_type": "complete_quiz",
        "target_count": 3,
        "reward_points": 40,
        "description": "Complete 3 quizzes with 80%+ accuracy",
        "icon": "✅"
    },
    {
        "challenge_type": "study_streak",
        "target_count": 1,
        "reward_points": 20,
        "description": "Maintain your daily study streak",
        "icon": "🔥"
    },
    {
        "challenge_type": "perfect_score",
        "target_count": 1,
        "reward_points": 100,
        "description": "Get a perfect score on any quiz",
        "icon": "🌟"
    },
    {
        "challenge_type": "study_time",
        "target_count": 30,
        "reward_points": 60,
        "description": "Study for at least 30 minutes",
        "icon": "⏱️"
    }
]


@router.get("/daily", response_model=List[DailyChallenge])
async def get_daily_challenges(current_user: dict = Depends(get_current_user)):
    """Get today's daily challenges"""
    db = get_database()
    challenges_collection = db.daily_challenges

    today = date.today().isoformat()

    # Check if challenges already exist for today
    cursor = challenges_collection.find({"date": today})
    existing_challenges = await cursor.to_list(length=10)

    if existing_challenges:
        return [
            DailyChallenge(
                _id=str(c["_id"]),
                date=c["date"],
                challenge_type=c["challenge_type"],
                target_count=c["target_count"],
                reward_points=c["reward_points"],
                description=c["description"],
                icon=c["icon"]
            )
            for c in existing_challenges
        ]

    # Generate new challenges for today (3 random challenges)
    selected_templates = random.sample(CHALLENGE_TEMPLATES, 3)

    new_challenges = []
    for template in selected_templates:
        challenge_doc = {
            "date": today,
            "challenge_type": template["challenge_type"],
            "target_count": template["target_count"],
            "reward_points": template["reward_points"],
            "description": template["description"],
            "icon": template["icon"],
            "created_at": datetime.utcnow()
        }
        result = await challenges_collection.insert_one(challenge_doc)
        challenge_doc["_id"] = result.inserted_id
        new_challenges.append(DailyChallenge(
            _id=str(challenge_doc["_id"]),
            date=challenge_doc["date"],
            challenge_type=challenge_doc["challenge_type"],
            target_count=challenge_doc["target_count"],
            reward_points=challenge_doc["reward_points"],
            description=challenge_doc["description"],
            icon=challenge_doc["icon"]
        ))

    return new_challenges


@router.get("/progress", response_model=List[UserChallengeProgress])
async def get_challenge_progress(current_user: dict = Depends(get_current_user)):
    """Get user's progress on today's challenges"""
    db = get_database()
    progress_collection = db.challenge_progress
    challenges_collection = db.daily_challenges

    today = date.today().isoformat()

    # Get today's challenges
    cursor = challenges_collection.find({"date": today})
    today_challenges = await cursor.to_list(length=10)

    if not today_challenges:
        return []

    # Get user's progress for each challenge
    progress_list = []
    for challenge in today_challenges:
        progress = await progress_collection.find_one({
            "user_id": current_user["_id"],
            "challenge_id": str(challenge["_id"]),
            "date": today
        })

        if progress:
            progress_list.append(UserChallengeProgress(
                _id=str(progress["_id"]),
                user_id=str(progress["user_id"]),
                challenge_id=str(progress["challenge_id"]),
                date=progress["date"],
                current_count=progress["current_count"],
                target_count=progress["target_count"],
                completed=progress["completed"],
                completed_at=progress.get("completed_at"),
                points_earned=progress.get("points_earned", 0)
            ))
        else:
            # Create initial progress entry
            progress_doc = {
                "user_id": current_user["_id"],
                "challenge_id": str(challenge["_id"]),
                "date": today,
                "current_count": 0,
                "target_count": challenge["target_count"],
                "completed": False,
                "points_earned": 0,
                "created_at": datetime.utcnow()
            }
            result = await progress_collection.insert_one(progress_doc)
            progress_doc["_id"] = result.inserted_id
            progress_list.append(UserChallengeProgress(
                _id=str(progress_doc["_id"]),
                user_id=str(progress_doc["user_id"]),
                challenge_id=str(progress_doc["challenge_id"]),
                date=progress_doc["date"],
                current_count=progress_doc["current_count"],
                target_count=progress_doc["target_count"],
                completed=progress_doc["completed"],
                points_earned=progress_doc.get("points_earned", 0)
            ))

    return progress_list


@router.post("/progress/update")
async def update_challenge_progress(
    challenge_id: str,
    increment: int = 1,
    current_user: dict = Depends(get_current_user)
):
    """Update progress on a challenge"""
    db = get_database()
    progress_collection = db.challenge_progress
    challenges_collection = db.daily_challenges
    users_collection = db.users

    today = date.today().isoformat()

    # Get challenge details
    challenge = await challenges_collection.find_one({"_id": ObjectId(challenge_id)})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Find or create progress entry
    progress = await progress_collection.find_one({
        "user_id": current_user["_id"],
        "challenge_id": challenge_id,
        "date": today
    })

    if not progress:
        progress = {
            "user_id": current_user["_id"],
            "challenge_id": challenge_id,
            "date": today,
            "current_count": 0,
            "target_count": challenge["target_count"],
            "completed": False,
            "points_earned": 0,
            "created_at": datetime.utcnow()
        }
        result = await progress_collection.insert_one(progress)
        progress["_id"] = result.inserted_id

    # Update progress
    new_count = progress["current_count"] + increment
    completed = new_count >= challenge["target_count"]

    update_doc = {
        "$set": {
            "current_count": new_count,
            "updated_at": datetime.utcnow()
        }
    }

    # If just completed, award points
    if completed and not progress["completed"]:
        update_doc["$set"]["completed"] = True
        update_doc["$set"]["completed_at"] = datetime.utcnow()
        update_doc["$set"]["points_earned"] = challenge["reward_points"]

        # Add points to user
        await users_collection.update_one(
            {"_id": current_user["_id"]},
            {
                "$inc": {
                    "total_points": challenge["reward_points"],
                    "points_this_week": challenge["reward_points"]
                }
            }
        )

    await progress_collection.update_one(
        {"_id": progress["_id"]},
        update_doc
    )

    # Get updated progress
    updated_progress = await progress_collection.find_one({"_id": progress["_id"]})

    return {
        "message": "Challenge progress updated",
        "current_count": updated_progress["current_count"],
        "target_count": updated_progress["target_count"],
        "completed": updated_progress.get("completed", False),
        "points_earned": updated_progress.get("points_earned", 0)
    }


@router.get("/streak", response_model=StudyStreak)
async def get_study_streak(current_user: dict = Depends(get_current_user)):
    """Get user's study streak"""
    db = get_database()
    streaks_collection = db.study_streaks

    streak = await streaks_collection.find_one({"user_id": current_user["_id"]})

    if not streak:
        # Create initial streak
        streak_doc = {
            "user_id": current_user["_id"],
            "current_streak": 0,
            "longest_streak": 0,
            "last_study_date": None,
            "study_dates": [],
            "created_at": datetime.utcnow()
        }
        result = await streaks_collection.insert_one(streak_doc)
        streak_doc["_id"] = result.inserted_id
        return StudyStreak(
            _id=str(streak_doc["_id"]),
            user_id=str(streak_doc["user_id"]),
            current_streak=streak_doc["current_streak"],
            longest_streak=streak_doc["longest_streak"],
            last_study_date=streak_doc["last_study_date"],
            study_dates=streak_doc["study_dates"]
        )

    return StudyStreak(
        _id=str(streak["_id"]),
        user_id=str(streak["user_id"]),
        current_streak=streak["current_streak"],
        longest_streak=streak["longest_streak"],
        last_study_date=streak.get("last_study_date"),
        study_dates=streak.get("study_dates", [])
    )


@router.post("/streak/update")
async def update_study_streak(current_user: dict = Depends(get_current_user)):
    """Update user's study streak (called when user studies)"""
    db = get_database()
    streaks_collection = db.study_streaks
    users_collection = db.users

    today = date.today().isoformat()

    streak = await streaks_collection.find_one({"user_id": current_user["_id"]})

    if not streak:
        # Create new streak
        streak_doc = {
            "user_id": current_user["_id"],
            "current_streak": 1,
            "longest_streak": 1,
            "last_study_date": today,
            "study_dates": [today],
            "created_at": datetime.utcnow()
        }
        await streaks_collection.insert_one(streak_doc)

        # Update user's streak count
        await users_collection.update_one(
            {"_id": current_user["_id"]},
            {"$set": {"study_streak": 1}}
        )

        return {
            "message": "Streak started",
            "current_streak": 1,
            "longest_streak": 1
        }

    # Check if already studied today
    if today in streak.get("study_dates", []):
        return {
            "message": "Already studied today",
            "current_streak": streak["current_streak"],
            "longest_streak": streak["longest_streak"]
        }

    # Check if streak continues
    last_date = date.fromisoformat(streak["last_study_date"]) if streak.get("last_study_date") else None
    today_date = date.today()

    if last_date:
        days_diff = (today_date - last_date).days

        if days_diff == 1:
            # Streak continues
            new_streak = streak["current_streak"] + 1
        elif days_diff > 1:
            # Streak broken
            new_streak = 1
        else:
            # Same day (already handled above)
            new_streak = streak["current_streak"]
    else:
        new_streak = 1

    new_longest = max(new_streak, streak["longest_streak"])

    # Update streak
    await streaks_collection.update_one(
        {"_id": streak["_id"]},
        {
            "$set": {
                "current_streak": new_streak,
                "longest_streak": new_longest,
                "last_study_date": today,
                "updated_at": datetime.utcnow()
            },
            "$addToSet": {"study_dates": today}
        }
    )

    # Update user's streak count
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"study_streak": new_streak}}
    )

    # Award bonus points for milestones
    bonus_points = 0
    if new_streak % 7 == 0:  # Weekly milestone
        bonus_points = 50
    elif new_streak % 30 == 0:  # Monthly milestone
        bonus_points = 200

    if bonus_points > 0:
        await users_collection.update_one(
            {"_id": current_user["_id"]},
            {
                "$inc": {
                    "total_points": bonus_points,
                    "streak_points": bonus_points
                }
            }
        )

    return {
        "message": "Streak updated",
        "current_streak": new_streak,
        "longest_streak": new_longest,
        "bonus_points": bonus_points
    }
