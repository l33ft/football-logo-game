"""
Club database model
"""
from sqlalchemy import Column, Integer, String
from core.database import Base


class Club(Base):
    """Football club model"""

    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    logo_path = Column(String, nullable=False)

    def __repr__(self):
        return f"<Club(id={self.id}, name='{self.name}')>"