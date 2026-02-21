"""
Game service - Contains all game business logic
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.game import Game, GameRound
from models.club import Club
from core.config import settings
from typing import Optional
import re


class GameService:
    """Service class for game logic and scoring"""

    def __init__(self, db: Session):
        self.db = db

    def start_new_game(self) -> Game:
        """
        Start a new game by creating a Game record and selecting random clubs
        """
        # Select random clubs
        random_clubs = (
            self.db.query(Club)
            .order_by(func.random())
            .limit(settings.LOGOS_PER_GAME)
            .all()
        )

        if len(random_clubs) < settings.LOGOS_PER_GAME:
            raise ValueError(f"Not enough clubs in database. Need at least {settings.LOGOS_PER_GAME}")

        # Create new game
        game = Game()
        self.db.add(game)
        self.db.flush()  # Get game ID

        # Create rounds for each club
        for club in random_clubs:
            round_obj = GameRound(
                game_id=game.id,
                club_id=club.id
            )
            self.db.add(round_obj)

        self.db.commit()
        self.db.refresh(game)

        return game

    def get_game(self, game_id: int) -> Optional[Game]:
        """Get game by ID"""
        return self.db.query(Game).filter(Game.id == game_id).first()

    def get_current_round(self, game: Game) -> Optional[GameRound]:
        """Get the current round for a game"""
        if game.finished or game.current_logo_index >= len(game.rounds):
            return None

        return game.rounds[game.current_logo_index]

    def calculate_blur_level(self, attempts_used: int) -> int:
        """
        Calculate blur level based on attempts used
        Returns CSS blur value in pixels
        """
        attempt_number = attempts_used + 1

        if attempt_number <= settings.MAX_ATTEMPTS:
            return settings.BLUR_LEVELS.get(attempt_number, 0)
        else:
            # After all attempts, no blur
            return settings.BLUR_LEVELS.get(settings.MAX_ATTEMPTS + 1, 0)

    def normalize_guess(self, guess: str) -> str:
        """
        Normalize user input for comparison
        - Strip whitespace
        - Convert to lowercase
        - Remove special characters except spaces
        """
        guess = guess.strip().lower()
        guess = re.sub(r'[^\w\s]', '', guess)
        return guess

    def check_guess(self, guess: str, correct_answer: str) -> bool:
        """
        Check if guess matches the correct answer
        Uses normalized comparison
        """
        normalized_guess = self.normalize_guess(guess)
        normalized_answer = self.normalize_guess(correct_answer)

        return normalized_guess == normalized_answer

    def calculate_points(self, attempts_used: int) -> int:
        """
        Calculate points based on attempts used
        Returns 0 if attempts exceed maximum
        """
        attempt_number = attempts_used + 1
        return settings.POINTS_MAPPING.get(attempt_number, 0)

    def process_guess(self, game: Game, guess: str) -> dict:
        """
        Process a guess for the current round
        Returns dict with result information
        """
        current_round = self.get_current_round(game)

        if not current_round:
            raise ValueError("No active round available")

        # Check if already guessed correctly or max attempts reached
        if current_round.guessed_correctly or current_round.attempts_used >= settings.MAX_ATTEMPTS:
            raise ValueError("Round already completed")

        # Increment attempts
        current_round.attempts_used += 1

        # Check guess
        is_correct = self.check_guess(guess, current_round.club.name)

        result = {
            "correct": is_correct,
            "points_earned": 0,
            "attempts_left": settings.MAX_ATTEMPTS - current_round.attempts_used,
            "finished_round": False,
            "correct_answer": None
        }

        if is_correct:
            # Calculate and award points
            points = self.calculate_points(current_round.attempts_used - 1)
            current_round.guessed_correctly = True
            current_round.points_earned = points
            game.total_score += points
            result["points_earned"] = points
            result["finished_round"] = True

            # Move to next round
            game.current_logo_index += 1

        elif current_round.attempts_used >= settings.MAX_ATTEMPTS:
            # No more attempts, reveal answer
            result["finished_round"] = True
            result["correct_answer"] = current_round.club.name

            # Move to next round
            game.current_logo_index += 1

        # Check if game is finished
        if game.current_logo_index >= settings.LOGOS_PER_GAME:
            game.finished = True

        self.db.commit()

        return result

    def get_game_summary(self, game: Game) -> dict:
        """
        Get complete game summary with all rounds
        """
        rounds_summary = []

        for round_obj in game.rounds:
            rounds_summary.append({
                "club_name": round_obj.club.name,
                "logo_path": round_obj.club.logo_path,
                "attempts_used": round_obj.attempts_used,
                "guessed_correctly": round_obj.guessed_correctly,
                "points_earned": round_obj.points_earned
            })

        return {
            "game_id": game.id,
            "total_score": game.total_score,
            "rounds": rounds_summary,
            "created_at": game.created_at
        }