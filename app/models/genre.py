from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.game import game_genres

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    games = relationship('Game', secondary=game_genres, back_populates='genres')
