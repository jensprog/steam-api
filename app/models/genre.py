from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from app.models.game import game_genres

"""
Genre model for the Steam Games API.

Defines the Genre entity with many-to-many relationship to Game.
"""


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

    games = relationship("Game", secondary=game_genres, back_populates="genres")
