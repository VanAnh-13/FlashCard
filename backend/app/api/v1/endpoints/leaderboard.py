"""
Leaderboard Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId

from app.models.leaderboard import (
    LeaderboardEntry,
    UserPoints,
    PointsUpdate,
    LeaderboardTimeframe
)
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


@router.get("/global", response_model=List[LeaderboardEntry])
async def get_global_leaderboard(
    limit: int = Query(100, le=500),
    timeframe: LeaderboardTimeframe = LeaderboardTimeframe.ALL_TIME,
    current_user: dict = Depends(get_current_user)
):
    """Get global leaderboard rankings"""
    db = get_database()
    users_collection = db.users

    # Build query based on timeframe
    match_query = {}
    if timeframe == LeaderboardTimeframe.WEEKLY:
        week_ago = datetime.utcnow() - timedelta(days=7)
        match_query = {"last_activity": {"$gte": week_ago}}
    elif timeframe == LeaderboardTimeframe.MONTHLY:
        month_ago = datetime.utcnow() - timedelta(days=30)
        match_query = {"last_activity": {"$gte": month_ago}}

    # Aggregate leaderboard data
    pipeline = [
        {"$match": match_query},
        {
            "$project": {
                "username": 1,
                "total_points": {"$ifNull": ["$total_points", 0]},
                "words_learned": {"$ifNull": ["$words_learned", 0]},
                "study_streak": {"$ifNull": ["$study_streak", 0]},
                "quizzes_completed": {"$ifNull": ["$quizzes_completed", 0]},
                "profile_picture": {"$ifNull": ["$profile_picture", ""]},
                "level": {"$ifNull": ["$level", "Beginner"]}
            }
        },
        {"$sort": {"total_points": -1, "words_learned": -1}},
        {"$limit": limit}
    ]

    users = await users_collection.aggregate(pipeline).to_list(length=limit)

    # Add rank to each user
    leaderboard = []
    for idx, user in enumerate(users, start=1):
        leaderboard.append(LeaderboardEntry(
            rank=idx,
            user_id=str(user["_id"]),
            username=user["username"],
            total_points=user["total_points"],
            words_learned=user["words_learned"],
            study_streak=user["study_streak"],
            quizzes_completed=user["quizzes_completed"],
            profile_picture=user.get("profile_picture", ""),
            level=user.get("level", "Beginner")
        ))

    return leaderboard


@router.get("/weekly", response_model=List[LeaderboardEntry])
async def get_weekly_leaderboard(
    limit: int = Query(100, le=500),
    current_user: dict = Depends(get_current_user)
):
    """Get weekly leaderboard rankings"""
    db = get_database()
    users_collection = db.users

    week_ago = datetime.utcnow() - timedelta(days=7)

    # Get users with weekly points
    pipeline = [
        {"$match": {"last_activity": {"$gte": week_ago}}},
        {
            "$project": {
                "username": 1,
                "points_this_week": {"$ifNull": ["$points_this_week", 0]},
                "words_learned_this_week": {"$ifNull": ["$words_learned_this_week", 0]},
                "study_streak": {"$ifNull": ["$study_streak", 0]},
                "quizzes_completed_this_week": {"$ifNull": ["$quizzes_completed_this_week", 0]},
                "profile_picture": {"$ifNull": ["$profile_picture", ""]},
                "level": {"$ifNull": ["$level", "Beginner"]}
            }
        },
        {"$sort": {"points_this_week": -1, "words_learned_this_week": -1}},
        {"$limit": limit}
    ]

    users = await users_collection.aggregate(pipeline).to_list(length=limit)

    leaderboard = []
    for idx, user in enumerate(users, start=1):
        leaderboard.append(LeaderboardEntry(
            rank=idx,
            user_id=str(user["_id"]),
            username=user["username"],
            total_points=user["points_this_week"],
            words_learned=user.get("words_learned_this_week", 0),
            study_streak=user["study_streak"],
            quizzes_completed=user.get("quizzes_completed_this_week", 0),
            profile_picture=user.get("profile_picture", ""),
            level=user.get("level", "Beginner")
        ))

    return leaderboard


@router.get("/friends", response_model=List[LeaderboardEntry])
async def get_friends_leaderboard(
    current_user: dict = Depends(get_current_user)
):
    """Get leaderboard for user's friends"""
    db = get_database()
    users_collection = db.users

    # Get current user's friends list
    friends = current_user.get("friends", [])

    if not friends:
        # Return only current user if no friends
        return [LeaderboardEntry(
            rank=1,
            user_id=str(current_user["_id"]),
            username=current_user["username"],
            total_points=current_user.get("total_points", 0),
            words_learned=current_user.get("words_learned", 0),
            study_streak=current_user.get("study_streak", 0),
            quizzes_completed=current_user.get("quizzes_completed", 0),
            profile_picture=current_user.get("profile_picture", ""),
            level=current_user.get("level", "Beginner")
        )]

    # Include current user in the list
    friend_ids = [ObjectId(fid) for fid in friends] + [current_user["_id"]]

    # Get friends' data
    pipeline = [
        {"$match": {"_id": {"$in": friend_ids}}},
        {
            "$project": {
                "username": 1,
                "total_points": {"$ifNull": ["$total_points", 0]},
                "words_learned": {"$ifNull": ["$words_learned", 0]},
                "study_streak": {"$ifNull": ["$study_streak", 0]},
                "quizzes_completed": {"$ifNull": ["$quizzes_completed", 0]},
                "profile_picture": {"$ifNull": ["$profile_picture", ""]},
                "level": {"$ifNull": ["$level", "Beginner"]}
            }
        },
        {"$sort": {"total_points": -1, "words_learned": -1}}
    ]

    users = await users_collection.aggregate(pipeline).to_list(length=len(friend_ids))

    leaderboard = []
    for idx, user in enumerate(users, start=1):
        leaderboard.append(LeaderboardEntry(
            rank=idx,
            user_id=str(user["_id"]),
            username=user["username"],
            total_points=user["total_points"],
            words_learned=user["words_learned"],
            study_streak=user["study_streak"],
            quizzes_completed=user["quizzes_completed"],
            profile_picture=user.get("profile_picture", ""),
            level=user.get("level", "Beginner")
        ))

    return leaderboard


@router.get("/my-rank")
async def get_my_rank(current_user: dict = Depends(get_current_user)):
    """Get current user's rank and points"""
    db = get_database()
    users_collection = db.users

    # Get total number of users
    total_users = await users_collection.count_documents({})

    # Get users with more points
    higher_ranked = await users_collection.count_documents({
        "total_points": {"$gt": current_user.get("total_points", 0)}
    })

    current_rank = higher_ranked + 1

    # Calculate percentile
    percentile = ((total_users - current_rank) / total_users * 100) if total_users > 0 else 0

    return {
        "rank": current_rank,
        "total_users": total_users,
        "percentile": round(percentile, 1),
        "points": UserPoints(
            total_points=current_user.get("total_points", 0),
            points_this_week=current_user.get("points_this_week", 0),
            flashcard_points=current_user.get("flashcard_points", 0),
            quiz_points=current_user.get("quiz_points", 0),
            streak_points=current_user.get("streak_points", 0)
        )
    }


@router.post("/points/add")
async def add_points(
    points_data: PointsUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Add points to user (internal use or admin)"""
    db = get_database()
    users_collection = db.users

    # Prepare update document
    update_doc = {
        "$inc": {
            "total_points": points_data.points,
            "points_this_week": points_data.points
        }
    }

    # Update specific point category if provided
    if points_data.category == "flashcard":
        update_doc["$inc"]["flashcard_points"] = points_data.points
    elif points_data.category == "quiz":
        update_doc["$inc"]["quiz_points"] = points_data.points
    elif points_data.category == "streak":
        update_doc["$inc"]["streak_points"] = points_data.points

    # Update last activity
    update_doc["$set"] = {"last_activity": datetime.utcnow()}

    # Update user points
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        update_doc
    )

    # Get updated user
    updated_user = await users_collection.find_one({"_id": current_user["_id"]})

    return {
        "message": "Points added successfully",
        "total_points": updated_user.get("total_points", 0),
        "points_added": points_data.points,
        "category": points_data.category
    }


@router.get("/top-learners", response_model=List[LeaderboardEntry])
async def get_top_learners(
    category: str = Query("words_learned", regex="^(words_learned|study_streak|quizzes_completed)$"),
    limit: int = Query(10, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get top learners by specific category"""
    db = get_database()
    users_collection = db.users

    # Build aggregation pipeline
    pipeline = [
        {
            "$project": {
                "username": 1,
                "total_points": {"$ifNull": ["$total_points", 0]},
                "words_learned": {"$ifNull": ["$words_learned", 0]},
                "study_streak": {"$ifNull": ["$study_streak", 0]},
                "quizzes_completed": {"$ifNull": ["$quizzes_completed", 0]},
                "profile_picture": {"$ifNull": ["$profile_picture", ""]},
                "level": {"$ifNull": ["$level", "Beginner"]}
            }
        },
        {"$sort": {category: -1, "total_points": -1}},
        {"$limit": limit}
    ]

    users = await users_collection.aggregate(pipeline).to_list(length=limit)

    leaderboard = []
    for idx, user in enumerate(users, start=1):
        leaderboard.append(LeaderboardEntry(
            rank=idx,
            user_id=str(user["_id"]),
            username=user["username"],
            total_points=user["total_points"],
            words_learned=user["words_learned"],
            study_streak=user["study_streak"],
            quizzes_completed=user["quizzes_completed"],
            profile_picture=user.get("profile_picture", ""),
            level=user.get("level", "Beginner")
        ))

    return leaderboard
