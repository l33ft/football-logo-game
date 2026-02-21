"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GameStartResponse(BaseModel):
    """Response when starting a new game"""
    game_id: int
    message: str
    total_logos: int


class CurrentLogoResponse(BaseModel):
    """Response for current logo state"""
    game_id: int
    logo_index: int
    total_logos: int
    logo_path: str
    blur_level: int
    attempts_left: int
    current_score: int
    finished: bool


class GuessRequest(BaseModel):
    """Request body for making a guess"""
    game_id: int
    guess: str = Field(..., min_length=1, max_length=100)


class GuessResponse(BaseModel):
    """Response after making a guess"""
    correct: bool
    points_earned: int
    attempts_left: int
    blur_level: int
    current_score: int
    correct_answer: Optional[str] = None
    finished_round: bool
    game_finished: bool


class RoundSummary(BaseModel):
    """Summary of a single round"""
    club_name: str
    logo_path: str
    attempts_used: int
    guessed_correctly: bool
    points_earned: int


class GameResultResponse(BaseModel):
    """Final game result"""
    game_id: int
    total_score: int
    rounds: list[RoundSummary]
    created_at: datetime

    class Config:
        from_attributes = True