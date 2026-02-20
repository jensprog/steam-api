from sqlalchemy import Column, Integer, String, Float, Boolean, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

game_developers = Table(
    'game_developers',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('developer_id', Integer, ForeignKey('developers.id'), primary_key=True)
)

game_genres = Table(
    'game_genres',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    release_date = Column(String)
    price = Column(Float, default=0.0)
    short_description = Column(Text)
    windows = Column(Boolean, default=False)
    mac = Column(Boolean, default=False)
    linux = Column(Boolean, default=False)
    metacritic_score = Column(Integer, default=0)
    positive = Column(Integer, default=0)
    negative = Column(Integer, default=0)
    average_playtime_forever = Column(Integer, default=0)
    estimated_owners = Column(String)
    header_image = Column(String)

    developers = relationship('Developer', secondary=game_developers, back_populates='games')
    genres = relationship('Genre', secondary=game_genres, back_populates='games')
