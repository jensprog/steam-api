from abc import ABC, abstractmethod
from typing import Optional
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