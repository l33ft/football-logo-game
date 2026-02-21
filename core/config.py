"""
Application configuration settings
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str = "sqlite:///./football_game.db"

    # Game settings
    LOGOS_PER_GAME: int = 10
    MAX_ATTEMPTS: int = 5

    # Scoring system
    POINTS_MAPPING: dict = {
        1: 10,  # First attempt
        2: 8,  # Second attempt
        3: 7,  # Third attempt
        4: 6,  # Fourth attempt
        5: 5,  # Fifth attempt
    }

    # Blur levels (CSS filter values)
    BLUR_LEVELS: dict = {
        1: 20,  # First attempt - heavily blurred
        2: 15,
        3: 10,
        4: 5,
        5: 2,  # Fifth attempt - slightly blurred
        6: 0,  # After all attempts - no blur
    }

    class Config:
        env_file = ".env"


settings = Settings()