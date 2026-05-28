from datetime import datetime
from typing import List, Optional, Tuple
from app.schemas.sync import SteamAppData
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.exceptions import ConstraintViolationError
from app.models.sync import SyncState
from app.repositories.interfaces.sync_repository import SyncRepositoryInterface
from app.models.game import Game
from app.models.developer import Developer
from app.models.genre import Genre


class SQLAlchemySyncRepository(SyncRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def get_last_sync_timestamp(self) -> Optional[datetime]:
        query = self.db.query(SyncState).first()

        if query is None:
            return None
        else:
            return query.last_sync_timestamp

    def update_last_sync_timestamp(self, timestamp: datetime) -> None:
        query = self.db.query(SyncState).first()

        if query is not None:
            query.last_sync_timestamp = timestamp
        else:
            new_state = SyncState(last_sync_timestamp=timestamp)
            self.db.add(new_state)

        self.db.commit()

    def upsert_game(self, game_data: SteamAppData) -> None:
        game_dict = game_data.model_dump()
        game_dict.pop("developers", None)
        game_dict.pop("genres", None)

        existing_game = self.db.query(Game).filter(Game.app_id == game_data.app_id).first()

        if existing_game is not None:
            for key, value in game_dict.items():
                setattr(existing_game, key, value)
        else:
            new_game = Game(**game_dict)
            self.db.add(new_game)

        game = existing_game if existing_game is not None else new_game

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
        self.db.commit()
