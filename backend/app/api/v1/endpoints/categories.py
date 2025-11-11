"""
Vocabulary Categories Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId
from typing import List, Optional

from app.models.categories import (
    Category,
    CategoryCreate,
    CategoryUpdate,
    UserCategoryProgress,
    CategoryStats
)
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


@router.get("/", response_model=List[Category])
async def get_categories(
    difficulty_level: Optional[str] = None,
    is_active: bool = True
):
    """Get all vocabulary categories"""
    db = get_database()
    categories_collection = db.categories

    # Build query
    query = {"is_active": is_active}
    if difficulty_level:
        query["difficulty_level"] = difficulty_level

    # Get categories sorted by sort_order
    cursor = categories_collection.find(query).sort("sort_order", 1)
    categories = await cursor.to_list(length=100)

    return [
        Category(
            _id=str(cat["_id"]),
            name=cat["name"],
            name_korean=cat["name_korean"],
            description=cat["description"],
            icon=cat.get("icon", "📚"),
            color=cat.get("color", "#2b6cee"),
            word_count=cat.get("word_count", 0),
            difficulty_level=cat.get("difficulty_level", "beginner"),
            is_active=cat.get("is_active", True),
            sort_order=cat.get("sort_order", 0)
        )
        for cat in categories
    ]


@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: str):
    """Get a specific category"""
    db = get_database()
    categories_collection = db.categories

    category = await categories_collection.find_one({"_id": ObjectId(category_id)})

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return Category(
        _id=str(category["_id"]),
        name=category["name"],
        name_korean=category["name_korean"],
        description=category["description"],
        icon=category.get("icon", "📚"),
        color=category.get("color", "#2b6cee"),
        word_count=category.get("word_count", 0),
        difficulty_level=category.get("difficulty_level", "beginner"),
        is_active=category.get("is_active", True),
        sort_order=category.get("sort_order", 0)
    )


@router.post("/", response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new vocabulary category"""
    db = get_database()
    categories_collection = db.categories

    # Check if category already exists
    existing = await categories_collection.find_one({"name": category_data.name})
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    # Get next sort order
    last_category = await categories_collection.find_one(
        {}, sort=[("sort_order", -1)]
    )
    next_sort_order = (last_category.get("sort_order", 0) + 1) if last_category else 0

    # Create category
    category_doc = {
        "name": category_data.name,
        "name_korean": category_data.name_korean,
        "description": category_data.description,
        "icon": category_data.icon,
        "color": category_data.color,
        "difficulty_level": category_data.difficulty_level,
        "word_count": 0,
        "is_active": True,
        "sort_order": next_sort_order,
        "created_at": datetime.utcnow(),
        "created_by": current_user["_id"]
    }

    result = await categories_collection.insert_one(category_doc)

    category_doc["_id"] = result.inserted_id

    return Category(
        _id=str(category_doc["_id"]),
        name=category_doc["name"],
        name_korean=category_doc["name_korean"],
        description=category_doc["description"],
        icon=category_doc["icon"],
        color=category_doc["color"],
        word_count=category_doc["word_count"],
        difficulty_level=category_doc["difficulty_level"],
        is_active=category_doc["is_active"],
        sort_order=category_doc["sort_order"]
    )


@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a category"""
    db = get_database()
    categories_collection = db.categories

    # Check if category exists
    category = await categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Build update document
    update_doc = {}
    if category_data.name is not None:
        update_doc["name"] = category_data.name
    if category_data.name_korean is not None:
        update_doc["name_korean"] = category_data.name_korean
    if category_data.description is not None:
        update_doc["description"] = category_data.description
    if category_data.icon is not None:
        update_doc["icon"] = category_data.icon
    if category_data.color is not None:
        update_doc["color"] = category_data.color
    if category_data.difficulty_level is not None:
        update_doc["difficulty_level"] = category_data.difficulty_level
    if category_data.is_active is not None:
        update_doc["is_active"] = category_data.is_active
    if category_data.sort_order is not None:
        update_doc["sort_order"] = category_data.sort_order

    if update_doc:
        update_doc["updated_at"] = datetime.utcnow()
        await categories_collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": update_doc}
        )

    # Get updated category
    updated_category = await categories_collection.find_one({"_id": ObjectId(category_id)})

    return Category(
        _id=str(updated_category["_id"]),
        name=updated_category["name"],
        name_korean=updated_category["name_korean"],
        description=updated_category["description"],
        icon=updated_category.get("icon", "📚"),
        color=updated_category.get("color", "#2b6cee"),
        word_count=updated_category.get("word_count", 0),
        difficulty_level=updated_category.get("difficulty_level", "beginner"),
        is_active=updated_category.get("is_active", True),
        sort_order=updated_category.get("sort_order", 0)
    )


@router.delete("/{category_id}")
async def delete_category(
    category_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a category (soft delete by setting is_active to False)"""
    db = get_database()
    categories_collection = db.categories

    result = await categories_collection.update_one(
        {"_id": ObjectId(category_id)},
        {
            "$set": {
                "is_active": False,
                "updated_at": datetime.utcnow()
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category deleted successfully"}


@router.get("/progress/all", response_model=List[UserCategoryProgress])
async def get_user_category_progress(current_user: dict = Depends(get_current_user)):
    """Get user's progress in all categories"""
    db = get_database()
    progress_collection = db.category_progress
    categories_collection = db.categories

    # Get all active categories
    categories = await categories_collection.find({"is_active": True}).to_list(length=100)

    progress_list = []
    for category in categories:
        # Get user's progress for this category
        progress = await progress_collection.find_one({
            "user_id": current_user["_id"],
            "category_id": str(category["_id"])
        })

        if progress:
            progress_list.append(UserCategoryProgress(
                _id=str(progress["_id"]),
                user_id=str(progress["user_id"]),
                category_id=str(progress["category_id"]),
                words_learned=progress.get("words_learned", 0),
                words_mastered=progress.get("words_mastered", 0),
                total_words=category.get("word_count", 0),
                completion_percentage=progress.get("completion_percentage", 0.0),
                last_studied=progress.get("last_studied"),
                study_streak=progress.get("study_streak", 0)
            ))
        else:
            # Create initial progress entry
            progress_doc = {
                "user_id": current_user["_id"],
                "category_id": str(category["_id"]),
                "words_learned": 0,
                "words_mastered": 0,
                "total_words": category.get("word_count", 0),
                "completion_percentage": 0.0,
                "last_studied": None,
                "study_streak": 0,
                "created_at": datetime.utcnow()
            }
            result = await progress_collection.insert_one(progress_doc)
            progress_doc["_id"] = result.inserted_id
            progress_list.append(UserCategoryProgress(
                _id=str(progress_doc["_id"]),
                user_id=str(progress_doc["user_id"]),
                category_id=str(progress_doc["category_id"]),
                words_learned=0,
                words_mastered=0,
                total_words=category.get("word_count", 0),
                completion_percentage=0.0,
                last_studied=None,
                study_streak=0
            ))

    return progress_list


@router.get("/stats/{category_id}", response_model=CategoryStats)
async def get_category_stats(
    category_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get user's statistics for a specific category"""
    db = get_database()
    categories_collection = db.categories
    progress_collection = db.category_progress
    flashcards_collection = db.flashcards
    srs_collection = db.srs_cards

    # Get category
    category = await categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Get user's progress
    progress = await progress_collection.find_one({
        "user_id": current_user["_id"],
        "category_id": category_id
    })

    # Get flashcards in this category
    flashcards = await flashcards_collection.find({
        "category": category["name"]
    }).to_list(length=1000)

    total_words = len(flashcards)

    # Get SRS cards for this category
    flashcard_ids = [str(fc["_id"]) for fc in flashcards]
    srs_cards = await srs_collection.find({
        "user_id": current_user["_id"],
        "flashcard_id": {"$in": flashcard_ids}
    }).to_list(length=1000)

    # Calculate stats
    words_learned = len(srs_cards)
    words_mastered = len([sc for sc in srs_cards if sc.get("interval", 0) >= 21])

    # Calculate average accuracy
    total_reviews = sum(sc.get("total_reviews", 0) for sc in srs_cards)
    correct_reviews = sum(sc.get("correct_reviews", 0) for sc in srs_cards)
    avg_accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0

    completion_percentage = (words_learned / total_words * 100) if total_words > 0 else 0

    return CategoryStats(
        category_id=category_id,
        category_name=category["name"],
        total_words=total_words,
        words_learned=words_learned,
        words_mastered=words_mastered,
        completion_percentage=round(completion_percentage, 1),
        average_accuracy=round(avg_accuracy, 1),
        study_time_minutes=progress.get("study_time_minutes", 0) if progress else 0,
        last_studied=progress.get("last_studied") if progress else None
    )


@router.post("/seed")
async def seed_categories(current_user: dict = Depends(get_current_user)):
    """Seed default categories"""
    db = get_database()
    categories_collection = db.categories

    # Check if categories already exist
    count = await categories_collection.count_documents({})
    if count > 0:
        return {"message": "Categories already seeded"}

    # Default categories
    default_categories = [
        {
            "name": "Greetings",
            "name_korean": "인사말",
            "description": "Common Korean greetings and polite expressions",
            "icon": "👋",
            "color": "#2b6cee",
            "difficulty_level": "beginner",
            "sort_order": 0
        },
        {
            "name": "Numbers",
            "name_korean": "숫자",
            "description": "Korean native and Sino-Korean numbers",
            "icon": "🔢",
            "color": "#50C878",
            "difficulty_level": "beginner",
            "sort_order": 1
        },
        {
            "name": "Food & Dining",
            "name_korean": "음식",
            "description": "Food items and dining vocabulary",
            "icon": "🍜",
            "color": "#ff9b85",
            "difficulty_level": "beginner",
            "sort_order": 2
        },
        {
            "name": "Family",
            "name_korean": "가족",
            "description": "Family members and relationships",
            "icon": "👨‍👩‍👧‍👦",
            "color": "#9b59b6",
            "difficulty_level": "beginner",
            "sort_order": 3
        },
        {
            "name": "Travel",
            "name_korean": "여행",
            "description": "Travel and transportation vocabulary",
            "icon": "✈️",
            "color": "#3498db",
            "difficulty_level": "intermediate",
            "sort_order": 4
        },
        {
            "name": "Business",
            "name_korean": "비즈니스",
            "description": "Business and workplace vocabulary",
            "icon": "💼",
            "color": "#e74c3c",
            "difficulty_level": "advanced",
            "sort_order": 5
        }
    ]

    for category in default_categories:
        category["word_count"] = 0
        category["is_active"] = True
        category["created_at"] = datetime.utcnow()
        category["created_by"] = current_user["_id"]

    await categories_collection.insert_many(default_categories)

    return {
        "message": "Categories seeded successfully",
        "count": len(default_categories)
    }
