from abc import ABC, abstractmethod
from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate, GameQueryParameters

"""Abstract interface for game data operations.
Returns raw domain models - business logic layer handles serialization.
Provides complete decoupling from database implementation."""


class GameRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, game_id: int) -> Game | None:
        """Find a game by its ID"""
        pass

    @abstractmethod
    def find_by_app_id(self, app_id: int) -> Game | None:
        """Find a game by its Steam app ID"""
        pass

    @abstractmethod
    def find_by_app_ids(self, app_ids: list[int]) -> list[Game]:
        """Find multiple games by their Steam app IDs in a single query"""
        pass

    @abstractmethod
    def find_filtered(self, params: GameQueryParameters) -> tuple[list[Game], int]:
        """Find filtered games and total count for pagination.

        Returns tuple of (games_list, total_count)
        """
        pass

    @abstractmethod
    def save(self, game_data: GameCreate, owner_id: int | None = None) -> Game:
        """Save a new game"""
        pass

    @abstractmethod
    def update(self, game_id: int, game_data: GameUpdate) -> Game | None:
        """Update an existing game"""
        pass

    @abstractmethod
    def remove(self, game_id: int) -> bool:
        """Remove a game by ID"""
        pass
