from abc import ABC, abstractmethod
from typing import Any
from app.schemas.developer import DeveloperQueryParameters

""" Abstract interface for statistic data operations.
Returns raw data for aggregations and filtering - business logic layer handles sorting and serialization"""


class StatsRepositoryInterface(ABC):
    @abstractmethod
    def get_price_distribution(self) -> list[tuple[str, int]]:
        """Get game count per price bucket, aggregated in the database"""
        pass

    @abstractmethod
    def get_owners_distribution(self) -> list[tuple[str, int]]:
        """Get game count per estimated-owners bucket, aggregated in the database"""
        pass

    @abstractmethod
    def get_genres_with_game_count(self) -> list[Any]:
        """Get all genres with their game count, ordered by count descending"""
        pass

    @abstractmethod
    def get_developers_with_game_count(self, params: DeveloperQueryParameters) -> tuple[list[Any], int]:
        """Get developers with their game count with pagination. Returns tuple of (rows, total_count)"""
        pass
