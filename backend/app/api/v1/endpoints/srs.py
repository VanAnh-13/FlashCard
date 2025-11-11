"""
Spaced Repetition System Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from bson import ObjectId

from app.models.spaced_repetition import (
    SpacedRepetitionCard,
    SRSReview,
    SRSDueCards,
    calculate_next_interval
)
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


@router.get("/due", response_model=SRSDueCards)
async def get_due_cards(current_user: dict = Depends(get_current_user)):
    """Get count of due cards for review"""
    db = get_database()
    srs_collection = db.srs_cards

    now = datetime.utcnow()
    today_end = datetime.combine(now.date(), datetime.max.time())
    week_end = now + timedelta(days=7)

    # Count due cards
    due_now_count = await srs_collection.count_documents({
        "user_id": current_user["_id"],
        "next_review": {"$lte": now}
    })

    due_today_count = await srs_collection.count_documents({
        "user_id": current_user["_id"],
        "next_review": {"$lte": today_end}
    })

    due_week_count = await srs_collection.count_documents({
        "user_id": current_user["_id"],
        "next_review": {"$lte": week_end}
    })

    total_count = await srs_collection.count_documents({
        "user_id": current_user["_id"]
    })

    return SRSDueCards(
        due_now=due_now_count,
        due_today=due_today_count,
        due_this_week=due_week_count,
        total_cards=total_count
    )


@router.get("/review")
async def get_cards_for_review(
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get cards that are due for review"""
    db = get_database()
    srs_collection = db.srs_cards
    flashcards_collection = db.flashcards

    # Get due SRS cards
    now = datetime.utcnow()
    cursor = srs_collection.find({
        "user_id": current_user["_id"],
        "next_review": {"$lte": now}
    }).sort("next_review", 1).limit(limit)

    srs_cards = await cursor.to_list(length=limit)

    # Get flashcard details
    flashcard_ids = [ObjectId(card["flashcard_id"]) for card in srs_cards]
    flashcards = await flashcards_collection.find({
        "_id": {"$in": flashcard_ids}
    }).to_list(length=limit)

    # Create flashcard lookup
    flashcard_map = {str(fc["_id"]): fc for fc in flashcards}

    # Combine SRS data with flashcard content
    review_cards = []
    for srs_card in srs_cards:
        flashcard = flashcard_map.get(srs_card["flashcard_id"])
        if flashcard:
            review_cards.append({
                "srs_id": str(srs_card["_id"]),
                "flashcard_id": srs_card["flashcard_id"],
                "korean": flashcard["korean"],
                "english": flashcard["english"],
                "example_korean": flashcard["example_korean"],
                "example_english": flashcard["example_english"],
                "interval": srs_card["interval"],
                "repetitions": srs_card["repetitions"]
            })

    return review_cards


@router.post("/review")
async def submit_review(
    review: SRSReview,
    current_user: dict = Depends(get_current_user)
):
    """Submit a review and update SRS data"""
    db = get_database()
    srs_collection = db.srs_cards

    # Validate quality rating
    if review.quality < 0 or review.quality > 5:
        raise HTTPException(status_code=400, detail="Quality must be between 0 and 5")

    # Find existing SRS card
    srs_card = await srs_collection.find_one({
        "user_id": current_user["_id"],
        "flashcard_id": review.flashcard_id
    })

    if srs_card:
        # Calculate next interval
        new_interval, new_ef, new_reps = calculate_next_interval(
            review.quality,
            srs_card["repetitions"],
            srs_card["easiness_factor"],
            srs_card["interval"]
        )

        # Update SRS card
        next_review = datetime.utcnow() + timedelta(days=new_interval)

        await srs_collection.update_one(
            {"_id": srs_card["_id"]},
            {
                "$set": {
                    "interval": new_interval,
                    "easiness_factor": new_ef,
                    "repetitions": new_reps,
                    "next_review": next_review,
                    "last_reviewed": datetime.utcnow()
                },
                "$inc": {
                    "total_reviews": 1,
                    "correct_reviews": 1 if review.quality >= 3 else 0
                }
            }
        )
    else:
        # Create new SRS card
        new_interval, new_ef, new_reps = calculate_next_interval(
            review.quality, 0, 2.5, 0
        )

        next_review = datetime.utcnow() + timedelta(days=new_interval)

        await srs_collection.insert_one({
            "user_id": current_user["_id"],
            "flashcard_id": review.flashcard_id,
            "easiness_factor": new_ef,
            "interval": new_interval,
            "repetitions": new_reps,
            "next_review": next_review,
            "last_reviewed": datetime.utcnow(),
            "total_reviews": 1,
            "correct_reviews": 1 if review.quality >= 3 else 0
        })

    return {
        "message": "Review submitted successfully",
        "next_review_in_days": new_interval
    }


@router.get("/stats")
async def get_srs_stats(current_user: dict = Depends(get_current_user)):
    """Get SRS statistics"""
    db = get_database()
    srs_collection = db.srs_cards

    # Get all user's SRS cards
    cards = await srs_collection.find({
        "user_id": current_user["_id"]
    }).to_list(length=10000)

    if not cards:
        return {
            "total_cards": 0,
            "average_easiness": 0,
            "average_interval": 0,
            "accuracy_rate": 0,
            "mature_cards": 0,
            "young_cards": 0,
            "new_cards": 0
        }

    total_cards = len(cards)
    avg_easiness = sum(c["easiness_factor"] for c in cards) / total_cards
    avg_interval = sum(c["interval"] for c in cards) / total_cards

    total_reviews = sum(c.get("total_reviews", 0) for c in cards)
    correct_reviews = sum(c.get("correct_reviews", 0) for c in cards)
    accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0

    # Classify cards
    mature_cards = len([c for c in cards if c["interval"] >= 21])  # 3+ weeks
    young_cards = len([c for c in cards if 1 <= c["interval"] < 21])
    new_cards = len([c for c in cards if c["interval"] == 0])

    return {
        "total_cards": total_cards,
        "average_easiness": round(avg_easiness, 2),
        "average_interval": round(avg_interval, 1),
        "accuracy_rate": round(accuracy, 1),
        "mature_cards": mature_cards,
        "young_cards": young_cards,
        "new_cards": new_cards
    }
