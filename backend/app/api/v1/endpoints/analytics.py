"""
Advanced Analytics Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta, date
from bson import ObjectId
from typing import List
from collections import defaultdict
import calendar

from app.models.analytics import (
    DailyActivity,
    WeeklyStats,
    MonthlyStats,
    LearningTrend,
    PerformanceMetrics,
    HeatmapData,
    StudyPattern,
    ProgressReport
)
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


@router.get("/daily", response_model=List[DailyActivity])
async def get_daily_activity(
    days: int = Query(30, le=365),
    current_user: dict = Depends(get_current_user)
):
    """Get daily activity for the last N days"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Calculate date range
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)

    # Get all sessions in range
    sessions = await sessions_collection.find({
        "user_id": current_user["_id"],
        "start_time": {
            "$gte": datetime.combine(start_date, datetime.min.time()),
            "$lte": datetime.combine(end_date, datetime.max.time())
        },
        "end_time": {"$ne": None}
    }).to_list(length=10000)

    # Group by date
    daily_data = defaultdict(lambda: {
        "words_learned": 0,
        "flashcards_reviewed": 0,
        "quizzes_completed": 0,
        "study_time_minutes": 0,
        "points_earned": 0,
        "total_answers": 0,
        "correct_answers": 0
    })

    for session in sessions:
        session_date = session["start_time"].date().isoformat()
        daily_data[session_date]["words_learned"] += session.get("words_learned", 0)
        daily_data[session_date]["flashcards_reviewed"] += session.get("flashcards_reviewed", 0)
        daily_data[session_date]["quizzes_completed"] += session.get("quizzes_completed", 0)
        daily_data[session_date]["study_time_minutes"] += session.get("duration_minutes", 0)
        daily_data[session_date]["points_earned"] += session.get("points_earned", 0)

        # Calculate accuracy
        total = session.get("total_answers", 0)
        correct = session.get("correct_answers", 0)
        daily_data[session_date]["total_answers"] += total
        daily_data[session_date]["correct_answers"] += correct

    # Create daily activity list
    result = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.isoformat()
        data = daily_data.get(date_str, {
            "words_learned": 0,
            "flashcards_reviewed": 0,
            "quizzes_completed": 0,
            "study_time_minutes": 0,
            "points_earned": 0,
            "total_answers": 0,
            "correct_answers": 0
        })

        accuracy = (
            data["correct_answers"] / data["total_answers"] * 100
            if data.get("total_answers", 0) > 0 else 0
        )

        result.append(DailyActivity(
            date=date_str,
            words_learned=data["words_learned"],
            flashcards_reviewed=data["flashcards_reviewed"],
            quizzes_completed=data["quizzes_completed"],
            study_time_minutes=data["study_time_minutes"],
            points_earned=data["points_earned"],
            accuracy_rate=round(accuracy, 1)
        ))

        current_date += timedelta(days=1)

    return result


@router.get("/weekly", response_model=WeeklyStats)
async def get_weekly_stats(current_user: dict = Depends(get_current_user)):
    """Get current week's statistics"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Calculate week range (Monday to Sunday)
    today = datetime.utcnow().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    # Get sessions for the week
    sessions = await sessions_collection.find({
        "user_id": current_user["_id"],
        "start_time": {
            "$gte": datetime.combine(week_start, datetime.min.time()),
            "$lte": datetime.combine(week_end, datetime.max.time())
        },
        "end_time": {"$ne": None}
    }).to_list(length=1000)

    # Calculate totals
    total_study_time = sum(s.get("duration_minutes", 0) for s in sessions)
    total_words_learned = sum(s.get("words_learned", 0) for s in sessions)
    total_flashcards = sum(s.get("flashcards_reviewed", 0) for s in sessions)
    total_quizzes = sum(s.get("quizzes_completed", 0) for s in sessions)
    total_points = sum(s.get("points_earned", 0) for s in sessions)

    # Calculate accuracy
    total_answers = sum(s.get("total_answers", 0) for s in sessions)
    correct_answers = sum(s.get("correct_answers", 0) for s in sessions)
    avg_accuracy = (correct_answers / total_answers * 100) if total_answers > 0 else 0

    # Study days
    study_dates = set(s["start_time"].date() for s in sessions)
    study_days = len(study_dates)

    # Daily breakdown
    daily_breakdown = await get_daily_activity(days=7, current_user=current_user)

    return WeeklyStats(
        week_start=week_start.isoformat(),
        week_end=week_end.isoformat(),
        total_study_time=total_study_time,
        total_words_learned=total_words_learned,
        total_flashcards_reviewed=total_flashcards,
        total_quizzes=total_quizzes,
        average_accuracy=round(avg_accuracy, 1),
        total_points=total_points,
        study_days=study_days,
        daily_breakdown=daily_breakdown[-7:]  # Last 7 days
    )


@router.get("/monthly", response_model=MonthlyStats)
async def get_monthly_stats(
    month: str = Query(None, regex=r"^\d{4}-\d{2}$"),
    current_user: dict = Depends(get_current_user)
):
    """Get monthly statistics (defaults to current month)"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Parse month or use current
    if month:
        year, month_num = map(int, month.split("-"))
    else:
        today = datetime.utcnow()
        year, month_num = today.year, today.month

    # Calculate month range
    month_start = date(year, month_num, 1)
    _, last_day = calendar.monthrange(year, month_num)
    month_end = date(year, month_num, last_day)

    # Get sessions for the month
    sessions = await sessions_collection.find({
        "user_id": current_user["_id"],
        "start_time": {
            "$gte": datetime.combine(month_start, datetime.min.time()),
            "$lte": datetime.combine(month_end, datetime.max.time())
        },
        "end_time": {"$ne": None}
    }).to_list(length=10000)

    # Calculate totals
    total_study_time = sum(s.get("duration_minutes", 0) for s in sessions)
    total_words_learned = sum(s.get("words_learned", 0) for s in sessions)
    total_flashcards = sum(s.get("flashcards_reviewed", 0) for s in sessions)
    total_quizzes = sum(s.get("quizzes_completed", 0) for s in sessions)
    total_points = sum(s.get("points_earned", 0) for s in sessions)

    # Calculate accuracy
    total_answers = sum(s.get("total_answers", 0) for s in sessions)
    correct_answers = sum(s.get("correct_answers", 0) for s in sessions)
    avg_accuracy = (correct_answers / total_answers * 100) if total_answers > 0 else 0

    # Study days
    study_dates = set(s["start_time"].date() for s in sessions)
    study_days = len(study_dates)

    # Weekly breakdown (simplified - just return empty for now)
    weekly_breakdown = []

    return MonthlyStats(
        month=f"{year}-{month_num:02d}",
        total_study_time=total_study_time,
        total_words_learned=total_words_learned,
        total_flashcards_reviewed=total_flashcards,
        total_quizzes=total_quizzes,
        average_accuracy=round(avg_accuracy, 1),
        total_points=total_points,
        study_days=study_days,
        weekly_breakdown=weekly_breakdown
    )


@router.get("/heatmap", response_model=List[HeatmapData])
async def get_study_heatmap(
    days: int = Query(365, le=365),
    current_user: dict = Depends(get_current_user)
):
    """Get study activity heatmap data"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Calculate date range
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)

    # Get all sessions in range
    sessions = await sessions_collection.find({
        "user_id": current_user["_id"],
        "start_time": {
            "$gte": datetime.combine(start_date, datetime.min.time()),
            "$lte": datetime.combine(end_date, datetime.max.time())
        },
        "end_time": {"$ne": None}
    }).to_list(length=10000)

    # Group by date and calculate intensity
    daily_minutes = defaultdict(int)
    for session in sessions:
        session_date = session["start_time"].date().isoformat()
        daily_minutes[session_date] += session.get("duration_minutes", 0)

    # Determine intensity levels
    if daily_minutes:
        max_minutes = max(daily_minutes.values())

        def calculate_intensity(minutes):
            if minutes == 0:
                return 0
            elif minutes <= max_minutes * 0.25:
                return 1
            elif minutes <= max_minutes * 0.5:
                return 2
            elif minutes <= max_minutes * 0.75:
                return 3
            else:
                return 4
    else:
        def calculate_intensity(minutes):
            return 0

    # Create heatmap data
    result = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.isoformat()
        minutes = daily_minutes.get(date_str, 0)

        result.append(HeatmapData(
            date=date_str,
            intensity=calculate_intensity(minutes)
        ))

        current_date += timedelta(days=1)

    return result


@router.get("/patterns", response_model=StudyPattern)
async def get_study_patterns(current_user: dict = Depends(get_current_user)):
    """Analyze user's study patterns"""
    db = get_database()
    sessions_collection = db.study_sessions

    # Get all sessions
    sessions = await sessions_collection.find({
        "user_id": current_user["_id"],
        "end_time": {"$ne": None}
    }).to_list(length=10000)

    if not sessions:
        return StudyPattern(
            most_active_hour=12,
            most_active_day="Monday",
            average_session_duration=0,
            preferred_study_type="mixed",
            consistency_score=0.0
        )

    # Analyze hour distribution
    hour_counts = defaultdict(int)
    for session in sessions:
        hour = session["start_time"].hour
        hour_counts[hour] += 1
    most_active_hour = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else 12

    # Analyze day distribution
    day_counts = defaultdict(int)
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for session in sessions:
        day = session["start_time"].weekday()
        day_counts[day] += 1
    most_active_day_idx = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else 0
    most_active_day = day_names[most_active_day_idx]

    # Average session duration
    avg_duration = sum(s.get("duration_minutes", 0) for s in sessions) / len(sessions)

    # Preferred study type
    type_counts = defaultdict(int)
    for session in sessions:
        session_type = session.get("session_type", "mixed")
        type_counts[session_type] += 1
    preferred_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else "mixed"

    # Consistency score (based on study streak and regularity)
    study_dates = sorted(set(s["start_time"].date() for s in sessions))
    if len(study_dates) > 1:
        # Calculate gaps between study days
        gaps = [(study_dates[i+1] - study_dates[i]).days for i in range(len(study_dates)-1)]
        avg_gap = sum(gaps) / len(gaps)
        # Lower average gap = higher consistency
        consistency = max(0, min(100, 100 - (avg_gap - 1) * 10))
    else:
        consistency = 0.0

    return StudyPattern(
        most_active_hour=most_active_hour,
        most_active_day=most_active_day,
        average_session_duration=int(avg_duration),
        preferred_study_type=preferred_type,
        consistency_score=round(consistency, 1)
    )


@router.get("/performance", response_model=PerformanceMetrics)
async def get_performance_metrics(current_user: dict = Depends(get_current_user)):
    """Get overall performance metrics"""
    db = get_database()
    sessions_collection = db.study_sessions
    srs_collection = db.srs_cards
    categories_collection = db.categories
    category_progress_collection = db.category_progress
    streaks_collection = db.study_streaks

    # Get total study time
    sessions = await sessions_collection.find({
        "user_id": current_user["_id"],
        "end_time": {"$ne": None}
    }).to_list(length=10000)

    total_study_time = sum(s.get("duration_minutes", 0) for s in sessions)

    # Get SRS stats
    srs_cards = await srs_collection.find({
        "user_id": current_user["_id"]
    }).to_list(length=10000)

    words_learned = len(srs_cards)
    words_mastered = len([sc for sc in srs_cards if sc.get("interval", 0) >= 21])

    # Calculate accuracy
    total_reviews = sum(sc.get("total_reviews", 0) for sc in srs_cards)
    correct_reviews = sum(sc.get("correct_reviews", 0) for sc in srs_cards)
    avg_accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0

    # Get category performance
    categories = await categories_collection.find({"is_active": True}).to_list(length=100)
    category_stats = []

    for category in categories[:6]:  # Limit to 6 categories
        progress = await category_progress_collection.find_one({
            "user_id": current_user["_id"],
            "category_id": str(category["_id"])
        })

        if progress:
            category_stats.append({
                "category_name": category["name"],
                "completion": progress.get("completion_percentage", 0),
                "words_learned": progress.get("words_learned", 0)
            })

    # Sort by completion
    category_stats.sort(key=lambda x: x["completion"], reverse=True)
    strongest = category_stats[:3] if len(category_stats) >= 3 else category_stats
    weakest = category_stats[-3:] if len(category_stats) >= 3 else []

    # Get streak info
    streak = await streaks_collection.find_one({"user_id": current_user["_id"]})
    current_streak = streak.get("current_streak", 0) if streak else 0
    longest_streak = streak.get("longest_streak", 0) if streak else 0

    # Get points and level
    total_points = current_user.get("total_points", 0)
    current_level = current_user.get("level", "Beginner")

    # Calculate next level points
    level_thresholds = {
        "Beginner": 500,
        "Intermediate": 2000,
        "Advanced": 5000,
        "Expert": 10000
    }
    next_level_points = level_thresholds.get(current_level, 0)

    return PerformanceMetrics(
        total_study_time=total_study_time,
        words_learned=words_learned,
        words_mastered=words_mastered,
        average_accuracy=round(avg_accuracy, 1),
        strongest_categories=strongest,
        weakest_categories=weakest,
        study_streak=current_streak,
        longest_streak=longest_streak,
        total_points=total_points,
        current_level=current_level,
        next_level_points=next_level_points
    )
