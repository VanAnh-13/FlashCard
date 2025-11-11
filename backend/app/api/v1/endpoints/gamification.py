"""
Gamification Endpoints - Achievements, Badges, Rewards
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId
from typing import List

from app.models.gamification import (
    Achievement,
    UserAchievement,
    Badge,
    UserBadge,
    Title,
    AchievementProgress
)
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


@router.get("/achievements", response_model=List[Achievement])
async def get_all_achievements(show_secret: bool = False):
    """Get all available achievements"""
    db = get_database()
    achievements_collection = db.achievements

    # Build query
    query = {}
    if not show_secret:
        query["is_secret"] = False

    cursor = achievements_collection.find(query).sort("difficulty", 1)
    achievements = await cursor.to_list(length=100)

    return [
        Achievement(
            _id=str(ach["_id"]),
            name=ach["name"],
            description=ach["description"],
            icon=ach["icon"],
            category=ach["category"],
            difficulty=ach["difficulty"],
            points_reward=ach["points_reward"],
            requirement_type=ach["requirement_type"],
            requirement_value=ach["requirement_value"],
            is_secret=ach.get("is_secret", False)
        )
        for ach in achievements
    ]


@router.get("/achievements/unlocked", response_model=List[UserAchievement])
async def get_unlocked_achievements(current_user: dict = Depends(get_current_user)):
    """Get user's unlocked achievements"""
    db = get_database()
    user_achievements_collection = db.user_achievements

    cursor = user_achievements_collection.find({
        "user_id": current_user["_id"]
    }).sort("unlocked_at", -1)

    unlocked = await cursor.to_list(length=1000)

    return [
        UserAchievement(
            _id=str(ua["_id"]),
            user_id=str(ua["user_id"]),
            achievement_id=ua["achievement_id"],
            achievement_name=ua["achievement_name"],
            achievement_icon=ua["achievement_icon"],
            unlocked_at=ua["unlocked_at"],
            points_earned=ua["points_earned"]
        )
        for ua in unlocked
    ]


@router.get("/achievements/progress", response_model=List[AchievementProgress])
async def get_achievement_progress(current_user: dict = Depends(get_current_user)):
    """Get user's progress towards all achievements"""
    db = get_database()
    achievements_collection = db.achievements
    user_achievements_collection = db.user_achievements
    srs_collection = db.srs_cards
    streaks_collection = db.study_streaks

    # Get all achievements
    achievements = await achievements_collection.find({}).to_list(length=100)

    # Get unlocked achievements
    unlocked_ids = set()
    cursor = user_achievements_collection.find({"user_id": current_user["_id"]})
    unlocked = await cursor.to_list(length=1000)
    unlocked_ids = {ua["achievement_id"] for ua in unlocked}

    # Get user stats
    srs_cards = await srs_collection.find({"user_id": current_user["_id"]}).to_list(length=10000)
    words_learned = len(srs_cards)
    words_mastered = len([sc for sc in srs_cards if sc.get("interval", 0) >= 21])

    streak_doc = await streaks_collection.find_one({"user_id": current_user["_id"]})
    current_streak = streak_doc.get("current_streak", 0) if streak_doc else 0
    longest_streak = streak_doc.get("longest_streak", 0) if streak_doc else 0

    quizzes_completed = current_user.get("quizzes_completed", 0)
    total_points = current_user.get("total_points", 0)

    # Map requirement types to current values
    user_stats = {
        "words_learned": words_learned,
        "words_mastered": words_mastered,
        "study_streak": current_streak,
        "longest_streak": longest_streak,
        "quizzes_completed": quizzes_completed,
        "total_points": total_points
    }

    # Calculate progress
    progress_list = []
    for ach in achievements:
        is_unlocked = str(ach["_id"]) in unlocked_ids
        current_value = user_stats.get(ach["requirement_type"], 0)
        target_value = ach["requirement_value"]
        progress_pct = min(100, (current_value / target_value * 100) if target_value > 0 else 0)

        progress_list.append(AchievementProgress(
            achievement_id=str(ach["_id"]),
            achievement_name=ach["name"],
            achievement_description=ach["description"],
            achievement_icon=ach["icon"],
            current_value=current_value,
            target_value=target_value,
            progress_percentage=round(progress_pct, 1),
            points_reward=ach["points_reward"],
            unlocked=is_unlocked
        ))

    return progress_list


@router.post("/achievements/check")
async def check_and_unlock_achievements(current_user: dict = Depends(get_current_user)):
    """Check and unlock achievements based on user's current stats"""
    db = get_database()
    achievements_collection = db.achievements
    user_achievements_collection = db.user_achievements
    users_collection = db.users
    srs_collection = db.srs_cards
    streaks_collection = db.study_streaks

    # Get user stats
    srs_cards = await srs_collection.find({"user_id": current_user["_id"]}).to_list(length=10000)
    words_learned = len(srs_cards)
    words_mastered = len([sc for sc in srs_cards if sc.get("interval", 0) >= 21])

    streak_doc = await streaks_collection.find_one({"user_id": current_user["_id"]})
    current_streak = streak_doc.get("current_streak", 0) if streak_doc else 0
    longest_streak = streak_doc.get("longest_streak", 0) if streak_doc else 0

    user_stats = {
        "words_learned": words_learned,
        "words_mastered": words_mastered,
        "study_streak": current_streak,
        "longest_streak": longest_streak,
        "quizzes_completed": current_user.get("quizzes_completed", 0),
        "total_points": current_user.get("total_points", 0)
    }

    # Get all achievements
    achievements = await achievements_collection.find({}).to_list(length=100)

    # Get already unlocked
    unlocked_ids = set()
    cursor = user_achievements_collection.find({"user_id": current_user["_id"]})
    unlocked = await cursor.to_list(length=1000)
    unlocked_ids = {ua["achievement_id"] for ua in unlocked}

    # Check for new unlocks
    newly_unlocked = []
    total_new_points = 0

    for ach in achievements:
        ach_id = str(ach["_id"])

        # Skip if already unlocked
        if ach_id in unlocked_ids:
            continue

        # Check if requirement met
        current_value = user_stats.get(ach["requirement_type"], 0)
        if current_value >= ach["requirement_value"]:
            # Unlock achievement
            unlock_doc = {
                "user_id": current_user["_id"],
                "achievement_id": ach_id,
                "achievement_name": ach["name"],
                "achievement_icon": ach["icon"],
                "unlocked_at": datetime.utcnow(),
                "points_earned": ach["points_reward"]
            }
            await user_achievements_collection.insert_one(unlock_doc)

            newly_unlocked.append({
                "name": ach["name"],
                "icon": ach["icon"],
                "points": ach["points_reward"]
            })

            total_new_points += ach["points_reward"]

    # Update user points
    if total_new_points > 0:
        await users_collection.update_one(
            {"_id": current_user["_id"]},
            {
                "$inc": {
                    "total_points": total_new_points,
                    "achievement_points": total_new_points
                }
            }
        )

    return {
        "message": f"Unlocked {len(newly_unlocked)} new achievements",
        "newly_unlocked": newly_unlocked,
        "total_points_earned": total_new_points
    }


@router.get("/badges", response_model=List[UserBadge])
async def get_user_badges(current_user: dict = Depends(get_current_user)):
    """Get user's earned badges"""
    db = get_database()
    user_badges_collection = db.user_badges

    cursor = user_badges_collection.find({
        "user_id": current_user["_id"]
    }).sort("earned_at", -1)

    badges = await cursor.to_list(length=1000)

    return [
        UserBadge(
            _id=str(b["_id"]),
            user_id=str(b["user_id"]),
            badge_id=b["badge_id"],
            badge_name=b["badge_name"],
            badge_icon=b["badge_icon"],
            badge_rarity=b["badge_rarity"],
            earned_at=b["earned_at"]
        )
        for b in badges
    ]


@router.get("/titles", response_model=List[Title])
async def get_available_titles():
    """Get all available titles"""
    db = get_database()
    titles_collection = db.titles

    cursor = titles_collection.find({}).sort("requirement_points", 1)
    titles = await cursor.to_list(length=100)

    return [
        Title(
            _id=str(t["_id"]),
            name=t["name"],
            name_korean=t["name_korean"],
            description=t["description"],
            requirement_points=t["requirement_points"],
            color=t.get("color", "#2b6cee"),
            icon=t.get("icon", "🏆")
        )
        for t in titles
    ]


@router.get("/titles/current")
async def get_current_title(current_user: dict = Depends(get_current_user)):
    """Get user's current title based on points"""
    db = get_database()
    titles_collection = db.titles

    user_points = current_user.get("total_points", 0)

    # Get all titles sorted by requirement
    cursor = titles_collection.find({}).sort("requirement_points", -1)
    titles = await cursor.to_list(length=100)

    # Find highest title user qualifies for
    current_title = None
    for title in titles:
        if user_points >= title["requirement_points"]:
            current_title = title
            break

    if not current_title:
        # Default title
        return {
            "title": "Beginner",
            "title_korean": "초보자",
            "color": "#2b6cee",
            "icon": "🌱",
            "points_to_next": titles[-1]["requirement_points"] if titles else 0
        }

    # Find next title
    next_title = None
    for title in reversed(titles):
        if title["requirement_points"] > user_points:
            next_title = title
            break

    return {
        "title": current_title["name"],
        "title_korean": current_title["name_korean"],
        "color": current_title.get("color", "#2b6cee"),
        "icon": current_title.get("icon", "🏆"),
        "points_to_next": next_title["requirement_points"] - user_points if next_title else 0,
        "next_title": next_title["name"] if next_title else None
    }


@router.post("/seed/achievements")
async def seed_achievements(current_user: dict = Depends(get_current_user)):
    """Seed default achievements"""
    db = get_database()
    achievements_collection = db.achievements

    # Check if already seeded
    count = await achievements_collection.count_documents({})
    if count > 0:
        return {"message": "Achievements already seeded"}

    # Default achievements
    default_achievements = [
        # Learning achievements
        {"name": "First Steps", "description": "Learn your first 10 Korean words", "icon": "🌱",
         "category": "learning", "difficulty": "bronze", "points_reward": 50,
         "requirement_type": "words_learned", "requirement_value": 10, "is_secret": False},

        {"name": "Vocabulary Builder", "description": "Learn 50 Korean words", "icon": "📚",
         "category": "learning", "difficulty": "silver", "points_reward": 100,
         "requirement_type": "words_learned", "requirement_value": 50, "is_secret": False},

        {"name": "Word Master", "description": "Learn 100 Korean words", "icon": "🎓",
         "category": "learning", "difficulty": "gold", "points_reward": 200,
         "requirement_type": "words_learned", "requirement_value": 100, "is_secret": False},

        {"name": "Korean Sage", "description": "Learn 500 Korean words", "icon": "🧙",
         "category": "learning", "difficulty": "platinum", "points_reward": 1000,
         "requirement_type": "words_learned", "requirement_value": 500, "is_secret": False},

        # Streak achievements
        {"name": "On a Roll", "description": "Maintain a 3-day study streak", "icon": "🔥",
         "category": "streak", "difficulty": "bronze", "points_reward": 30,
         "requirement_type": "study_streak", "requirement_value": 3, "is_secret": False},

        {"name": "Consistency King", "description": "Maintain a 7-day study streak", "icon": "👑",
         "category": "streak", "difficulty": "silver", "points_reward": 70,
         "requirement_type": "study_streak", "requirement_value": 7, "is_secret": False},

        {"name": "Unstoppable", "description": "Maintain a 30-day study streak", "icon": "⚡",
         "category": "streak", "difficulty": "gold", "points_reward": 300,
         "requirement_type": "study_streak", "requirement_value": 30, "is_secret": False},

        {"name": "Legendary Dedication", "description": "Maintain a 100-day study streak", "icon": "💫",
         "category": "streak", "difficulty": "platinum", "points_reward": 1000,
         "requirement_type": "study_streak", "requirement_value": 100, "is_secret": False},

        # Mastery achievements
        {"name": "Quick Learner", "description": "Master 10 words", "icon": "⭐",
         "category": "mastery", "difficulty": "bronze", "points_reward": 100,
         "requirement_type": "words_mastered", "requirement_value": 10, "is_secret": False},

        {"name": "Expert Learner", "description": "Master 50 words", "icon": "🌟",
         "category": "mastery", "difficulty": "silver", "points_reward": 250,
         "requirement_type": "words_mastered", "requirement_value": 50, "is_secret": False},

        # Quiz achievements
        {"name": "Quiz Novice", "description": "Complete 10 quizzes", "icon": "✍️",
         "category": "learning", "difficulty": "bronze", "points_reward": 50,
         "requirement_type": "quizzes_completed", "requirement_value": 10, "is_secret": False},

        {"name": "Quiz Master", "description": "Complete 50 quizzes", "icon": "🎯",
         "category": "learning", "difficulty": "silver", "points_reward": 150,
         "requirement_type": "quizzes_completed", "requirement_value": 50, "is_secret": False},
    ]

    for ach in default_achievements:
        ach["created_at"] = datetime.utcnow()

    await achievements_collection.insert_many(default_achievements)

    return {
        "message": "Achievements seeded successfully",
        "count": len(default_achievements)
    }


@router.post("/seed/titles")
async def seed_titles(current_user: dict = Depends(get_current_user)):
    """Seed default titles"""
    db = get_database()
    titles_collection = db.titles

    # Check if already seeded
    count = await titles_collection.count_documents({})
    if count > 0:
        return {"message": "Titles already seeded"}

    # Default titles
    default_titles = [
        {"name": "Beginner", "name_korean": "초보자", "description": "Just starting the journey",
         "requirement_points": 0, "color": "#9E9E9E", "icon": "🌱"},

        {"name": "Apprentice", "name_korean": "견습생", "description": "Learning the basics",
         "requirement_points": 500, "color": "#4CAF50", "icon": "📖"},

        {"name": "Scholar", "name_korean": "학자", "description": "Building knowledge",
         "requirement_points": 2000, "color": "#2196F3", "icon": "🎓"},

        {"name": "Expert", "name_korean": "전문가", "description": "Advanced learner",
         "requirement_points": 5000, "color": "#9C27B0", "icon": "🏆"},

        {"name": "Master", "name_korean": "마스터", "description": "Mastered Korean vocabulary",
         "requirement_points": 10000, "color": "#FF9800", "icon": "👑"},

        {"name": "Grandmaster", "name_korean": "그랜드마스터", "description": "Elite Korean speaker",
         "requirement_points": 20000, "color": "#F44336", "icon": "💎"},
    ]

    for title in default_titles:
        title["created_at"] = datetime.utcnow()

    await titles_collection.insert_many(default_titles)

    return {
        "message": "Titles seeded successfully",
        "count": len(default_titles)
    }
