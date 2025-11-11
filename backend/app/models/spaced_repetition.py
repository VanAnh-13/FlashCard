"""
Spaced Repetition System Model
Implements SM-2 algorithm for optimal learning intervals
"""

from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional


class SpacedRepetitionCard(BaseModel):
    """SRS card model"""
    id: str = Field(alias="_id")
    user_id: str
    flashcard_id: str
    easiness_factor: float = 2.5  # E-Factor (2.5 is default)
    interval: int = 0  # Days until next review
    repetitions: int = 0  # Number of successful repetitions
    next_review: datetime  # When to review next
    last_reviewed: Optional[datetime] = None
    total_reviews: int = 0
    correct_reviews: int = 0

    class Config:
        populate_by_name = True


class SRSReview(BaseModel):
    """SRS review submission"""
    flashcard_id: str
    quality: int  # 0-5 rating (0=complete blackout, 5=perfect response)


class SRSDueCards(BaseModel):
    """Due cards response"""
    due_now: int
    due_today: int
    due_this_week: int
    total_cards: int


def calculate_next_interval(
    quality: int,
    repetitions: int,
    easiness_factor: float,
    interval: int
) -> tuple[int, float, int]:
    """
    Calculate next review interval using SM-2 algorithm

    Returns: (new_interval, new_easiness_factor, new_repetitions)
    """
    # Update easiness factor
    new_ef = easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

    # Ensure EF doesn't go below 1.3
    if new_ef < 1.3:
        new_ef = 1.3

    # Calculate new interval
    if quality < 3:  # Incorrect response
        new_repetitions = 0
        new_interval = 1  # Review again tomorrow
    else:  # Correct response
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = int(interval * new_ef)

        new_repetitions = repetitions + 1

    return new_interval, new_ef, new_repetitions
