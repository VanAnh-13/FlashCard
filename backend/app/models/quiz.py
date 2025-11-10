"""
Quiz Model
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class QuizQuestion(BaseModel):
    """Quiz question model"""
    korean: str
    correct_answer: str
    options: List[str]


class QuizAnswer(BaseModel):
    """Quiz answer submission"""
    question: str
    user_answer: str
    correct_answer: str


class QuizSubmission(BaseModel):
    """Quiz submission model"""
    answers: List[QuizAnswer]


class QuizResult(BaseModel):
    """Quiz result model"""
    id: str = Field(alias="_id")
    user_id: str
    score: float
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    answers: List[dict]
    completed_at: datetime

    class Config:
        populate_by_name = True


class QuizStats(BaseModel):
    """Quiz statistics"""
    total_quizzes: int
    average_score: float
    best_score: float
    total_questions_answered: int
    accuracy_rate: float
