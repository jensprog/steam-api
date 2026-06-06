# SQLAlchemy implementation of SyncRepositoryInterface, handles sync state and game upserts in the database.
from datetime import datetime
from app.schemas.sync import SteamAppData
from sqlalchemy.orm import Session
from app.models.sync import SyncState
from app.repositories.interfaces.sync_repository import SyncRepositoryInterface
from app.models.game import Game
from app.models.developer import Developer
from app.models.genre import Genre


class SQLAlchemySyncRepository(SyncRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    # Returns the timestamp of the last completed sync, or None if no sync has run yet.
    def get_last_sync_timestamp(self) -> datetime | None:
        query = self.db.query(SyncState).first()

        if query is None:
            return None
        else:
            return query.last_sync_timestamp

    # Updates the last sync timestamp, or creates the sync state row if it does not exist.
    def update_last_sync_timestamp(self, timestamp: datetime) -> None:
        query = self.db.query(SyncState).first()

        if query is not None:
            query.last_sync_timestamp = timestamp
        else:
            new_state = SyncState(last_sync_timestamp=timestamp)
            self.db.add(new_state)

        self.db.commit()

    # Returns all app IDs currently stored in the database.
    def get_all_app_ids(self) -> set[int]:
        rows = self.db.query(Game.app_id).all()
        return {row[0] for row in rows}

    # Returns the last processed app ID from a gap sync, used to resume if interrupted.
    def get_gap_sync_checkpoint(self) -> int | None:
        state = self.db.query(SyncState).first()
        return state.gap_sync_checkpoint if state is not None else None

    # Saves the current gap sync checkpoint, or clears it by passing None when sync is complete.
    def set_gap_sync_checkpoint(self, app_id: int | None) -> None:
        state = self.db.query(SyncState).first()
        if state is not None:
            state.gap_sync_checkpoint = app_id
        else:
            self.db.add(SyncState(gap_sync_checkpoint=app_id))
        self.db.commit()

    # Updates existing game if any updates have occurred, if game does not exist in db, insert game.
    def upsert_game(self, game_data: SteamAppData) -> None:
        try:
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
                self.db.flush()
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
        except Exception:
            self.db.rollback()
            raise
