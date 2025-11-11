"""
Study Sessions Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from bson import ObjectId
from typing import List

from app.models.challenges import StudySession
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


@router.post("/start")
async def start_study_session(
    session_type: str = "mixed",  # flashcard, quiz, mixed
    current_user: dict = Depends(get_current_user)
):
    """Start a new study session"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Check if there's an active session
    active_session = await sessions_collection.find_one({
        "user_id": current_user["_id"],
        "end_time": None
    })

    if active_session:
        return {
            "message": "Active session already exists",
            "session_id": str(active_session["_id"]),
            "start_time": active_session["start_time"].isoformat()
        }

    # Create new session
    session_doc = {
        "user_id": current_user["_id"],
        "start_time": datetime.utcnow(),
        "end_time": None,
        "duration_minutes": 0,
        "flashcards_reviewed": 0,
        "quizzes_completed": 0,
        "words_learned": 0,
        "accuracy_rate": 0.0,
        "points_earned": 0,
        "session_type": session_type,
        "created_at": datetime.utcnow()
    }

    result = await sessions_collection.insert_one(session_doc)

    return {
        "message": "Study session started",
        "session_id": str(result.inserted_id),
        "start_time": session_doc["start_time"].isoformat()
    }


@router.post("/end/{session_id}")
async def end_study_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """End a study session"""
    db = get_database()
    sessions_collection = db.study_sessions
    users_collection = db.users

    # Find session
    session = await sessions_collection.find_one({
        "_id": ObjectId(session_id),
        "user_id": current_user["_id"]
    })

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.get("end_time"):
        raise HTTPException(status_code=400, detail="Session already ended")

    # Calculate duration
    end_time = datetime.utcnow()
    duration = (end_time - session["start_time"]).total_seconds() / 60  # in minutes

    # Calculate points based on duration (1 point per minute, max 60 points per session)
    duration_points = min(int(duration), 60)

    # Update session
    await sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {
            "$set": {
                "end_time": end_time,
                "duration_minutes": int(duration),
                "points_earned": duration_points,
                "updated_at": datetime.utcnow()
            }
        }
    )

    # Add points to user
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {
            "$inc": {
                "total_points": duration_points,
                "points_this_week": duration_points
            }
        }
    )

    # Get updated session
    updated_session = await sessions_collection.find_one({"_id": ObjectId(session_id)})

    return {
        "message": "Study session ended",
        "session_id": session_id,
        "duration_minutes": int(duration),
        "points_earned": duration_points,
        "flashcards_reviewed": updated_session["flashcards_reviewed"],
        "quizzes_completed": updated_session["quizzes_completed"],
        "words_learned": updated_session["words_learned"],
        "accuracy_rate": updated_session["accuracy_rate"]
    }


@router.post("/update/{session_id}")
async def update_session_activity(
    session_id: str,
    flashcards_reviewed: int = 0,
    quizzes_completed: int = 0,
    words_learned: int = 0,
    correct_answers: int = 0,
    total_answers: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """Update activity during a study session"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Find session
    session = await sessions_collection.find_one({
        "_id": ObjectId(session_id),
        "user_id": current_user["_id"]
    })

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.get("end_time"):
        raise HTTPException(status_code=400, detail="Cannot update ended session")

    # Calculate new accuracy rate
    new_total_answers = session.get("total_answers", 0) + total_answers
    new_correct_answers = session.get("correct_answers", 0) + correct_answers
    accuracy_rate = (new_correct_answers / new_total_answers * 100) if new_total_answers > 0 else 0

    # Update session
    await sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {
            "$inc": {
                "flashcards_reviewed": flashcards_reviewed,
                "quizzes_completed": quizzes_completed,
                "words_learned": words_learned,
                "correct_answers": correct_answers,
                "total_answers": total_answers
            },
            "$set": {
                "accuracy_rate": round(accuracy_rate, 1),
                "updated_at": datetime.utcnow()
            }
        }
    )

    return {
        "message": "Session updated",
        "flashcards_reviewed": session["flashcards_reviewed"] + flashcards_reviewed,
        "quizzes_completed": session["quizzes_completed"] + quizzes_completed,
        "words_learned": session["words_learned"] + words_learned,
        "accuracy_rate": round(accuracy_rate, 1)
    }


@router.get("/active")
async def get_active_session(current_user: dict = Depends(get_current_user)):
    """Get user's active study session"""
    db = get_database()
    sessions_collection = db.study_sessions

    session = await sessions_collection.find_one({
        "user_id": current_user["_id"],
        "end_time": None
    })

    if not session:
        return {"active_session": None}

    # Calculate current duration
    duration = (datetime.utcnow() - session["start_time"]).total_seconds() / 60

    return {
        "active_session": {
            "session_id": str(session["_id"]),
            "start_time": session["start_time"].isoformat(),
            "duration_minutes": int(duration),
            "flashcards_reviewed": session["flashcards_reviewed"],
            "quizzes_completed": session["quizzes_completed"],
            "words_learned": session["words_learned"],
            "accuracy_rate": session["accuracy_rate"],
            "session_type": session["session_type"]
        }
    }


@router.get("/history", response_model=List[StudySession])
async def get_session_history(
    limit: int = 30,
    current_user: dict = Depends(get_current_user)
):
    """Get user's study session history"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Get completed sessions
    cursor = sessions_collection.find({
        "user_id": current_user["_id"],
        "end_time": {"$ne": None}
    }).sort("start_time", -1).limit(limit)

    sessions = await cursor.to_list(length=limit)

    return [
        StudySession(
            _id=str(s["_id"]),
            user_id=str(s["user_id"]),
            start_time=s["start_time"],
            end_time=s.get("end_time"),
            duration_minutes=s["duration_minutes"],
            flashcards_reviewed=s["flashcards_reviewed"],
            quizzes_completed=s["quizzes_completed"],
            words_learned=s["words_learned"],
            accuracy_rate=s["accuracy_rate"],
            points_earned=s.get("points_earned", 0),
            session_type=s.get("session_type", "mixed")
        )
        for s in sessions
    ]


@router.get("/stats")
async def get_session_stats(current_user: dict = Depends(get_current_user)):
    """Get user's study session statistics"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Get all user's completed sessions
    cursor = sessions_collection.find({
        "user_id": current_user["_id"],
        "end_time": {"$ne": None}
    })

    sessions = await cursor.to_list(length=10000)

    if not sessions:
        return {
            "total_sessions": 0,
            "total_study_time": 0,
            "average_session_duration": 0,
            "total_flashcards_reviewed": 0,
            "total_quizzes_completed": 0,
            "total_words_learned": 0,
            "average_accuracy": 0,
            "this_week_sessions": 0,
            "this_week_study_time": 0
        }

    # Calculate stats
    total_sessions = len(sessions)
    total_study_time = sum(s["duration_minutes"] for s in sessions)
    avg_duration = total_study_time / total_sessions if total_sessions > 0 else 0

    total_flashcards = sum(s["flashcards_reviewed"] for s in sessions)
    total_quizzes = sum(s["quizzes_completed"] for s in sessions)
    total_words = sum(s["words_learned"] for s in sessions)

    # Calculate average accuracy
    sessions_with_accuracy = [s for s in sessions if s.get("accuracy_rate", 0) > 0]
    avg_accuracy = (
        sum(s["accuracy_rate"] for s in sessions_with_accuracy) / len(sessions_with_accuracy)
        if sessions_with_accuracy else 0
    )

    # This week stats
    week_ago = datetime.utcnow() - timedelta(days=7)
    this_week_sessions = [s for s in sessions if s["start_time"] >= week_ago]
    this_week_count = len(this_week_sessions)
    this_week_time = sum(s["duration_minutes"] for s in this_week_sessions)

    return {
        "total_sessions": total_sessions,
        "total_study_time": total_study_time,
        "average_session_duration": round(avg_duration, 1),
        "total_flashcards_reviewed": total_flashcards,
        "total_quizzes_completed": total_quizzes,
        "total_words_learned": total_words,
        "average_accuracy": round(avg_accuracy, 1),
        "this_week_sessions": this_week_count,
        "this_week_study_time": this_week_time
    }
