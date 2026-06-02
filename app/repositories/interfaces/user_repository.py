from abc import ABC, abstractmethod
from app.models.user import User

""" Abstract interface for user register and login"""


class UserRepositoryInterface(ABC):
    @abstractmethod
    def find_by_username(self, username: str) -> User | None:
        """Find user by its username"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """Find user by its email"""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Saves a new user"""
        pass
