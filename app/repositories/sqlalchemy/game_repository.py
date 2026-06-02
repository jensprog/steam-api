from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.exceptions import ConstraintViolationError
from app.repositories.interfaces.game_repository import GameRepositoryInterface
from app.models.game import Game
from app.models.developer import Developer
from app.models.genre import Genre
from app.schemas.game import GameCreate, GameUpdate, GameQueryParameters

"""
SQLAlchemy implementation of game repository interface.

Handles database operations for games including CRUD operations,
filtering, and many-to-many relationship management.
"""


class SQLAlchemyGameRepository(GameRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, game_id: int) -> Game | None:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def find_by_app_id(self, app_id: int) -> Game | None:
        return self.db.query(Game).filter(Game.app_id == app_id).first()

    def find_filtered(self, params: GameQueryParameters) -> tuple[list[Game], int]:
        query = self.db.query(Game)

        if params.developer:
            query = query.filter(Game.developers.any(name=params.developer))
        if params.genre:
            query = query.filter(Game.genres.any(name=params.genre))
        if params.search:
            query = query.filter(Game.name.ilike(f"%{params.search}%"))

        total_games = query.count()
        games = query.order_by(Game.id).limit(params.limit).offset((params.page - 1) * params.limit).all()

        return games, total_games

    def save(self, game_data: GameCreate, owner_id: int | None = None) -> Game:
        game_dict = game_data.model_dump()
        game_dict.pop("developers", None)
        game_dict.pop("genres", None)
        if owner_id is not None:
            game_dict["owner_id"] = owner_id
        new_game = Game(**game_dict)

        for name in game_data.developers:
            dev = self.db.query(Developer).filter(Developer.name == name).first()
            if not dev:
                dev = Developer(name=name)
                self.db.add(dev)
                self.db.flush()
            new_game.developers.append(dev)

        for name in game_data.genres:
            genre = self.db.query(Genre).filter(Genre.name == name).first()
            if not genre:
                genre = Genre(name=name)
                self.db.add(genre)
                self.db.flush()
            new_game.genres.append(genre)

        try:
            self.db.add(new_game)
            self.db.commit()
            self.db.refresh(new_game)
            return new_game
        except IntegrityError as e:
            self.db.rollback()
            raise ConstraintViolationError(f"Failed to create game - constraint violation: {str(e)}")

    def update(self, game_id: int, game_data: GameUpdate) -> Game | None:
        game = self.db.query(Game).filter(Game.id == game_id).first()
        if not game:
            return None

        game_dict = game_data.model_dump(exclude_unset=True)
        game_dict.pop("developers", None)
        game_dict.pop("genres", None)

        for key, value in game_dict.items():
            setattr(game, key, value)

        if game_data.developers is not None:
            game.developers.clear()
            for name in game_data.developers:
                dev = self.db.query(Developer).filter(Developer.name == name).first()
                if not dev:
                    dev = Developer(name=name)
                    self.db.add(dev)
                    self.db.flush()
                game.developers.append(dev)

        if game_data.genres is not None:
            game.genres.clear()
            for name in game_data.genres:
                genre = self.db.query(Genre).filter(Genre.name == name).first()
                if not genre:
                    genre = Genre(name=name)
                    self.db.add(genre)
                    self.db.flush()
                game.genres.append(genre)
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
