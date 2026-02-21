"""
Game API router - Handles all game-related endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import settings
from services.game_service import GameService
from schemas.game import (
    GameStartResponse,
    CurrentLogoResponse,
    GuessRequest,
    GuessResponse,
    GameResultResponse
)

router = APIRouter()


@router.post("/game/start", response_model=GameStartResponse)
def start_game(db: Session = Depends(get_db)):
    """
    Start a new game session
    Selects 10 random logos and creates game record
    """
    try:
        service = GameService(db)
        game = service.start_new_game()

        return GameStartResponse(
            game_id=game.id,
            message="Game started successfully",
            total_logos=settings.LOGOS_PER_GAME
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start game"
        )


@router.get("/game/current", response_model=CurrentLogoResponse)
def get_current_logo(game_id: int, db: Session = Depends(get_db)):
    """
    Get current logo state
    Returns logo path, blur level, attempts left, etc.
    Does NOT return the correct answer
    """
    service = GameService(db)
    game = service.get_game(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    current_round = service.get_current_round(game)

    if not current_round:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active round available"
        )

    blur_level = service.calculate_blur_level(current_round.attempts_used)
    attempts_left = settings.MAX_ATTEMPTS - current_round.attempts_used

    return CurrentLogoResponse(
        game_id=game.id,
        logo_index=game.current_logo_index + 1,
        total_logos=settings.LOGOS_PER_GAME,
        logo_path=current_round.club.logo_path,
        blur_level=blur_level,
        attempts_left=attempts_left,
        current_score=game.total_score,
        finished=game.finished
    )


@router.post("/game/guess", response_model=GuessResponse)
def make_guess(request: GuessRequest, db: Session = Depends(get_db)):
    """
    Process a guess for the current logo
    Returns whether guess was correct and updates game state
    """
    service = GameService(db)
    game = service.get_game(request.game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    if game.finished:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game already finished"
        )

    try:
        result = service.process_guess(game, request.guess)

        # Get updated round info for blur level
        if not result["finished_round"]:
            current_round = service.get_current_round(game)
            blur_level = service.calculate_blur_level(current_round.attempts_used)
        else:
            blur_level = 0

        return GuessResponse(
            correct=result["correct"],
            points_earned=result["points_earned"],
            attempts_left=result["attempts_left"],
            blur_level=blur_level,
            current_score=game.total_score,
            correct_answer=result.get("correct_answer"),
            finished_round=result["finished_round"],
            game_finished=game.finished
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process guess"
        )


@router.get("/game/result", response_model=GameResultResponse)
def get_game_result(game_id: int, db: Session = Depends(get_db)):
    """
    Get final game results
    Returns total score and summary of all rounds
    """
    service = GameService(db)
    game = service.get_game(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    if not game.finished:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game not finished yet"
        )

    summary = service.get_game_summary(game)
    return GameResultResponse(**summary)