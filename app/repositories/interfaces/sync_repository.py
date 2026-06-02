# Abstract interface for sync repository, defining methods for managing sync state and upserting games.
from abc import ABC, abstractmethod
from datetime import datetime
from app.schemas.sync import SteamAppData


class SyncRepositoryInterface(ABC):
    @abstractmethod
    def get_last_sync_timestamp(self) -> datetime | None:
        pass

    @abstractmethod
    def update_last_sync_timestamp(self, timestamp: datetime) -> None:
        pass

    @abstractmethod
    def upsert_game(self, game_data: SteamAppData) -> None:
        pass

    @abstractmethod
    def get_all_app_ids(self) -> set[int]:
        pass

    @abstractmethod
    def get_gap_sync_checkpoint(self) -> int | None:
        pass

    @abstractmethod
    def set_gap_sync_checkpoint(self, app_id: int | None) -> None:
        pass
