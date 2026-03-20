from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.game import game_developers

"""
Developer model for the Steam Games API.

Defines the Developer entity with many-to-many relationship to Game.
"""


class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    games = relationship("Game", secondary=game_developers, back_populates="developers")
