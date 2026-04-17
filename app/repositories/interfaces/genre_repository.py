from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.models.genre import Genre
from app.models.game import Game
from app.schemas.genre import GenreQueryParameters

"""Abstract interface for genre data operations.
Returns raw domain models - business logic layer handles serialization.
Provides complete decoupling from database implementation."""


class GenreRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, genre_id: int) -> Optional[Genre]:
        """Find a genre by its ID"""
        pass

    @abstractmethod
    def find_filtered(self, params: GenreQueryParameters) -> Tuple[List[Genre], int]:
        """Find filtered genres"""
        pass

    @abstractmethod
    def find_games_by_genre(self, genre_id: int, params: GenreQueryParameters) -> Tuple[List[Game], int]:
        """Find paginated games belonging to a genre"""
        pass
