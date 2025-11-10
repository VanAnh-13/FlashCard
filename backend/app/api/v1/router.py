"""
API V1 Router - Combines all endpoint routers
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, flashcards, quiz

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(flashcards.router, prefix="/flashcards", tags=["Flashcards"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
