"""
Flashcard Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime

from app.models.flashcard import FlashcardResponse, FlashcardCreate, ProgressUpdate
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


# Sample flashcards data
SAMPLE_FLASHCARDS = [
    {"korean": "안녕하세요", "english": "Hello", "example_korean": "안녕하세요, 만나서 반갑습니다.", "example_english": "Hello, nice to meet you.", "category": "greetings", "difficulty": 1},
    {"korean": "감사합니다", "english": "Thank you", "example_korean": "도와주셔서 감사합니다.", "example_english": "Thank you for helping me.", "category": "greetings", "difficulty": 1},
    {"korean": "사랑해요", "english": "I love you", "example_korean": "나는 너를 정말 사랑해요.", "example_english": "I really love you.", "category": "emotions", "difficulty": 1},
    {"korean": "미안해요", "english": "I'm sorry", "example_korean": "늦어서 미안해요.", "example_english": "I'm sorry for being late.", "category": "apologies", "difficulty": 1},
    {"korean": "괜찮아요", "english": "It's okay", "example_korean": "걱정하지 마세요, 괜찮아요.", "example_english": "Don't worry, it's okay.", "category": "reassurance", "difficulty": 1},
    {"korean": "물", "english": "Water", "example_korean": "물 한 잔 주세요.", "example_english": "Please give me a glass of water.", "category": "food", "difficulty": 1},
    {"korean": "밥", "english": "Rice / Meal", "example_korean": "밥 먹었어요?", "example_english": "Did you eat?", "category": "food", "difficulty": 1},
    {"korean": "학교", "english": "School", "example_korean": "학교에 가요.", "example_english": "I'm going to school.", "category": "places", "difficulty": 1},
    {"korean": "친구", "english": "Friend", "example_korean": "제 친구예요.", "example_english": "This is my friend.", "category": "relationships", "difficulty": 1},
    {"korean": "가족", "english": "Family", "example_korean": "가족이 중요해요.", "example_english": "Family is important.", "category": "relationships", "difficulty": 1},
]


@router.get("/", response_model=List[FlashcardResponse])
async def get_flashcards(
    skip: int = 0,
    limit: int = 50,
    category: str = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all flashcards"""
    db = get_database()
    flashcards_collection = db.flashcards

    # Build query
    query = {}
    if category:
        query["category"] = category

    # Get flashcards
    cursor = flashcards_collection.find(query).skip(skip).limit(limit)
    flashcards = await cursor.to_list(length=limit)

    # Convert ObjectId to string
    for flashcard in flashcards:
        flashcard["_id"] = str(flashcard["_id"])

    return [FlashcardResponse(**fc) for fc in flashcards]


@router.get("/{flashcard_id}", response_model=FlashcardResponse)
async def get_flashcard(
    flashcard_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific flashcard"""
    db = get_database()
    flashcards_collection = db.flashcards

    flashcard = await flashcards_collection.find_one({"_id": ObjectId(flashcard_id)})

    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    flashcard["_id"] = str(flashcard["_id"])
    return FlashcardResponse(**flashcard)


@router.post("/seed")
async def seed_flashcards():
    """Seed database with sample flashcards (development only)"""
    db = get_database()
    flashcards_collection = db.flashcards

    # Clear existing flashcards
    await flashcards_collection.delete_many({})

    # Insert sample flashcards
    flashcards_to_insert = []
    for fc in SAMPLE_FLASHCARDS:
        fc["created_at"] = datetime.utcnow()
        fc["updated_at"] = datetime.utcnow()
        flashcards_to_insert.append(fc)

    result = await flashcards_collection.insert_many(flashcards_to_insert)

    return {
        "message": f"Seeded {len(result.inserted_ids)} flashcards",
        "count": len(result.inserted_ids)
    }


@router.post("/progress")
async def update_progress(
    progress_data: ProgressUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update user progress on a flashcard"""
    db = get_database()
    progress_collection = db.user_progress

    # Find existing progress
    existing_progress = await progress_collection.find_one({
        "user_id": current_user["_id"],
        "flashcard_id": progress_data.flashcard_id
    })

    if existing_progress:
        # Update existing progress
        update_data = progress_data.dict(exclude_unset=True, exclude={"flashcard_id"})
        update_data["times_reviewed"] = existing_progress.get("times_reviewed", 0) + 1
        update_data["last_reviewed_at"] = datetime.utcnow()

        await progress_collection.update_one(
            {"_id": existing_progress["_id"]},
            {"$set": update_data}
        )
    else:
        # Create new progress
        progress_doc = {
            "user_id": current_user["_id"],
            "flashcard_id": progress_data.flashcard_id,
            "known": progress_data.known or False,
            "review_later": progress_data.review_later or False,
            "times_reviewed": 1,
            "last_reviewed_at": datetime.utcnow(),
            "accuracy": 0.0
        }

        await progress_collection.insert_one(progress_doc)

    return {"message": "Progress updated successfully"}


@router.get("/progress/my")
async def get_my_progress(current_user: dict = Depends(get_current_user)):
    """Get current user's progress"""
    db = get_database()
    progress_collection = db.user_progress

    cursor = progress_collection.find({"user_id": current_user["_id"]})
    progress_list = await cursor.to_list(length=1000)

    # Convert ObjectId to string
    for progress in progress_list:
        progress["_id"] = str(progress["_id"])

    return progress_list
