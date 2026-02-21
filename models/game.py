"""
Game and GameRound database models
"""
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class Game(Base):
    """Game session model"""

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    current_logo_index = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    finished = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    rounds = relationship("GameRound", back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game(id={self.id}, score={self.total_score}, finished={self.finished})>"


class GameRound(Base):
    """Individual logo round in a game"""

    __tablename__ = "game_rounds"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    attempts_used = Column(Integer, default=0)
    guessed_correctly = Column(Boolean, default=False)
    points_earned = Column(Integer, default=0)

    # Relationships
    game = relationship("Game", back_populates="rounds")
    club = relationship("Club")

    def __repr__(self):
        return f"<GameRound(id={self.id}, club_id={self.club_id}, attempts={self.attempts_used})>"