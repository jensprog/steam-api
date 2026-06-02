from abc import ABC, abstractmethod
from app.models.developer import Developer
from app.schemas.developer import DeveloperQueryParameters

"""Abstract interface for developer data operations.
Returns raw domain models - business logic layer handles serialization.
Provides complete decoupling from database implementation."""


class DeveloperRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, developer_id: int) -> Developer | None:
        """Find a developer by its ID"""
        pass

    @abstractmethod
    def find_filtered(self, params: DeveloperQueryParameters) -> tuple[list[Developer], int]:
        """Find filtered developers"""
        pass
