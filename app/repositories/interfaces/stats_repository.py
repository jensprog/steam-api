from abc import ABC, abstractmethod
from typing import Any
from app.schemas.developer import DeveloperQueryParameters

""" Abstract interface for statistic data operations.
Returns raw data for aggregations and filtering - business logic layer handles sorting and serialization"""


class StatsRepositoryInterface(ABC):
    @abstractmethod
    def get_games_with_price(self) -> list[Any]:
        """Get all games with their prices"""
        pass

    @abstractmethod
    def get_games_with_owners(self) -> list[Any]:
        """Get all games with their estimated owners"""
        pass

    @abstractmethod
    def get_genres_with_game_count(self) -> list[Any]:
        """Get all genres with their game count, ordered by count descending"""
        pass

    @abstractmethod
    def get_developers_with_game_count(self, params: DeveloperQueryParameters) -> tuple[list[Any], int]:
        """Get developers with their game count with pagination. Returns tuple of (rows, total_count)"""
        pass
