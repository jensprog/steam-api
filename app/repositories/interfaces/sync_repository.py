# Abstract interface for sync repository, defining methods for managing sync state and upserting games.
from abc import ABC, abstractmethod
from typing import Optional, Set
from datetime import datetime
from app.schemas.sync import SteamAppData


class SyncRepositoryInterface(ABC):
    @abstractmethod
    def get_last_sync_timestamp(self) -> Optional[datetime]:
        pass

    @abstractmethod
    def update_last_sync_timestamp(self, timestamp: datetime) -> None:
        pass

    @abstractmethod
    def upsert_game(self, game_data: SteamAppData) -> None:
        pass

    @abstractmethod
    def get_all_app_ids(self) -> Set[int]:
        pass

    @abstractmethod
    def get_gap_sync_checkpoint(self) -> Optional[int]:
        pass

    @abstractmethod
    def set_gap_sync_checkpoint(self, app_id: Optional[int]) -> None:
        pass
