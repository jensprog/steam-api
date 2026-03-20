from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.interfaces import (
    GameRepositoryInterface,
    ConstraintViolationError,
)
from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate, GameQueryParameters

"""
SQLAlchemy implementation of game repository interface.

Handles database operations for games including CRUD operations,
filtering, and many-to-many relationship management.
"""


class SQLAlchemyGameRepository(GameRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, game_id: int) -> Optional[Game]:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def find_filtered(self, params: GameQueryParameters) -> Tuple[List[Game], int]:
        query = self.db.query(Game)

        if params.developer:
            query = query.filter(Game.developers.any(name=params.developer))
        if params.genre:
            query = query.filter(Game.genres.any(name=params.genre))
        if params.search:
            query = query.filter(Game.name.ilike(f"%{params.search}%"))

        total_games = query.count()
        games = query.limit(params.limit).offset((params.page - 1) * params.limit).all()

        return games, total_games

    def save(self, game_data: GameCreate) -> Game:
        new_game = Game(**game_data.model_dump())
        try:
            self.db.add(new_game)
            self.db.commit()
            self.db.refresh(new_game)
            return new_game
        except IntegrityError as e:
            self.db.rollback()
            raise ConstraintViolationError(f"Failed to create game - constraint violation: {str(e)}")

    def update(self, game_id: int, game_data: GameUpdate) -> Optional[Game]:
        game = self.db.query(Game).filter(Game.id == game_id).first()
        if not game:
            return None

        for key, value in game_data.model_dump(exclude_unset=True).items():
            setattr(game, key, value)

        try:
            self.db.commit()
            self.db.refresh(game)
            return game
        except IntegrityError as e:
            self.db.rollback()
            raise ConstraintViolationError(f"Failed to update game - constraint violation: {str(e)}")

    def remove(self, game_id: int) -> bool:
        game = self.db.query(Game).filter(Game.id == game_id).first()
        if not game:
            return False

        try:
            self.db.delete(game)
            self.db.commit()
            return True
        except IntegrityError as e:
            self.db.rollback()
            raise ConstraintViolationError(f"Failed to delete game - referenced by other data: {str(e)}")
