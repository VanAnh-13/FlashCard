"""
Advanced Analytics Models
"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class DailyActivity(BaseModel):
    """Daily activity stats"""
    date: str  # YYYY-MM-DD
    words_learned: int = 0
    flashcards_reviewed: int = 0
    quizzes_completed: int = 0
    study_time_minutes: int = 0
    points_earned: int = 0
    accuracy_rate: float = 0.0


class WeeklyStats(BaseModel):
    """Weekly statistics"""
    week_start: str  # YYYY-MM-DD
    week_end: str
    total_study_time: int
    total_words_learned: int
    total_flashcards_reviewed: int
    total_quizzes: int
    average_accuracy: float
    total_points: int
    study_days: int
    daily_breakdown: List[DailyActivity]


class MonthlyStats(BaseModel):
    """Monthly statistics"""
    month: str  # YYYY-MM
    total_study_time: int
    total_words_learned: int
    total_flashcards_reviewed: int
    total_quizzes: int
    average_accuracy: float
    total_points: int
    study_days: int
    weekly_breakdown: List[WeeklyStats]


class LearningTrend(BaseModel):
    """Learning trend over time"""
    period: str  # week, month, quarter, year
    trend_data: List[Dict[str, any]]
    growth_rate: float
    insights: List[str]


class PerformanceMetrics(BaseModel):
    """Overall performance metrics"""
    total_study_time: int  # minutes
    words_learned: int
    words_mastered: int
    average_accuracy: float
    strongest_categories: List[Dict[str, any]]
    weakest_categories: List[Dict[str, any]]
    study_streak: int
    longest_streak: int
    total_points: int
    current_level: str
    next_level_points: int


class HeatmapData(BaseModel):
    """Heatmap data for study activity"""
    date: str
    intensity: int  # 0-4 scale


class StudyPattern(BaseModel):
    """Study patterns analysis"""
    most_active_hour: int
    most_active_day: str
    average_session_duration: int
    preferred_study_type: str  # flashcard, quiz, mixed
    consistency_score: float  # 0-100


class ProgressReport(BaseModel):
    """Comprehensive progress report"""
    report_period: str  # week, month, quarter, year
    start_date: str
    end_date: str
    performance_metrics: PerformanceMetrics
    learning_trends: LearningTrend
    study_patterns: StudyPattern
    achievements_unlocked: List[str]
    recommendations: List[str]
