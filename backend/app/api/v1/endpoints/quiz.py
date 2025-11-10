"""
Quiz Endpoints
"""

from fastapi import APIRouter, Depends
from typing import List
import random
from datetime import datetime
from bson import ObjectId

from app.models.quiz import QuizQuestion, QuizSubmission, QuizResult, QuizStats
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


@router.get("/questions", response_model=List[QuizQuestion])
async def get_quiz_questions(
    count: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get random quiz questions"""
    db = get_database()
    flashcards_collection = db.flashcards

    # Get all flashcards
    flashcards = await flashcards_collection.find().to_list(length=1000)

    if len(flashcards) < count:
        count = len(flashcards)

    # Select random flashcards
    selected_flashcards = random.sample(flashcards, count)

    # Create questions
    questions = []
    for fc in selected_flashcards:
        # Get other random flashcards for wrong options
        other_flashcards = [f for f in flashcards if f["_id"] != fc["_id"]]
        wrong_options = random.sample(other_flashcards, min(3, len(other_flashcards)))

        # Create options list
        options = [fc["english"]] + [f["english"] for f in wrong_options]
        random.shuffle(options)

        questions.append(QuizQuestion(
            korean=fc["korean"],
            correct_answer=fc["english"],
            options=options
        ))

    return questions


@router.post("/submit", response_model=QuizResult)
async def submit_quiz(
    submission: QuizSubmission,
    current_user: dict = Depends(get_current_user)
):
    """Submit quiz answers"""
    db = get_database()
    quiz_results_collection = db.quiz_results

    # Calculate score
    correct_count = 0
    answers_detail = []

    for answer in submission.answers:
        is_correct = answer.user_answer == answer.correct_answer
        if is_correct:
            correct_count += 1

        answers_detail.append({
            "question": answer.question,
            "user_answer": answer.user_answer,
            "correct_answer": answer.correct_answer,
            "is_correct": is_correct
        })

    total_questions = len(submission.answers)
    score = (correct_count / total_questions * 100) if total_questions > 0 else 0

    # Save quiz result
    quiz_result = {
        "user_id": current_user["_id"],
        "score": score,
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "incorrect_answers": total_questions - correct_count,
        "answers": answers_detail,
        "completed_at": datetime.utcnow()
    }

    result = await quiz_results_collection.insert_one(quiz_result)
    quiz_result["_id"] = str(result.inserted_id)

    return QuizResult(**quiz_result)


@router.get("/results", response_model=List[QuizResult])
async def get_quiz_results(
    skip: int = 0,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get user's quiz results"""
    db = get_database()
    quiz_results_collection = db.quiz_results

    cursor = quiz_results_collection.find(
        {"user_id": current_user["_id"]}
    ).sort("completed_at", -1).skip(skip).limit(limit)

    results = await cursor.to_list(length=limit)

    # Convert ObjectId to string
    for result in results:
        result["_id"] = str(result["_id"])

    return [QuizResult(**r) for r in results]


@router.get("/stats", response_model=QuizStats)
async def get_quiz_stats(current_user: dict = Depends(get_current_user)):
    """Get user's quiz statistics"""
    db = get_database()
    quiz_results_collection = db.quiz_results

    results = await quiz_results_collection.find(
        {"user_id": current_user["_id"]}
    ).to_list(length=1000)

    if not results:
        return QuizStats(
            total_quizzes=0,
            average_score=0.0,
            best_score=0.0,
            total_questions_answered=0,
            accuracy_rate=0.0
        )

    total_quizzes = len(results)
    total_score = sum(r["score"] for r in results)
    best_score = max(r["score"] for r in results)
    total_questions = sum(r["total_questions"] for r in results)
    total_correct = sum(r["correct_answers"] for r in results)

    return QuizStats(
        total_quizzes=total_quizzes,
        average_score=total_score / total_quizzes,
        best_score=best_score,
        total_questions_answered=total_questions,
        accuracy_rate=(total_correct / total_questions * 100) if total_questions > 0 else 0.0
    )
