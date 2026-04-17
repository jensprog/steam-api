from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.repositories.interfaces.genre_repository import GenreRepositoryInterface
from app.models.game import Game
from app.models.genre import Genre
from app.schemas.genre import GenreQueryParameters

"""
SQLAlchemy implementation of genre repository interface.

Handles database operations for genre GET operations including filtering genres and filtering games belonging to genres
"""


class SQLAlchemyGenreRepository(GenreRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, genre_id: int) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.id == genre_id).first()

    def find_filtered(self, params: GenreQueryParameters) -> Tuple[List[Genre], int]:
        query = self.db.query(Genre)

        if params.game:
            query = query.filter(Genre.games.any(name=params.game))
        if params.developer:
            query = query.filter(Genre.games.any(Game.developers.any(name=params.developer)))
        if params.search:
            query = query.filter(Genre.name.ilike(f"%{params.search}%"))

        total_genres = query.count()
        genres = query.limit(params.limit).offset((params.page - 1) * params.limit).all()

        return genres, total_genres

    def find_games_by_genre(self, genre_id: int, params: GenreQueryParameters) -> Tuple[List[Game], int]:
        games = self.db.query(Game).filter(Game.genres.any(id=genre_id))

        total_games = games.count()
        games = games.limit(params.limit).offset((params.page - 1) * params.limit).all()

        return games, total_games
