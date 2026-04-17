from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.models.developer import Developer
from app.schemas.developer import DeveloperQueryParameters

"""Abstract interface for developer data operations.
Returns raw domain models - business logic layer handles serialization.
Provides complete decoupling from database implementation."""


class DeveloperRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, developer_id: int) -> Optional[Developer]:
        """Find a developer by its ID"""
        pass

    @abstractmethod
    def find_filtered(self, params: DeveloperQueryParameters) -> Tuple[List[Developer], int]:
        """Find filtered developers"""
        pass
