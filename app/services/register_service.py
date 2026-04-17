from app.models.user import User
from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.schemas.auth import UserRegister
from app.core.security import get_password_hash

"""
User registration service.

Handles new user creation with password hashing and
duplicate username validation.
"""


def register_user(user_repo: UserRepositoryInterface, user_data: UserRegister) -> User:
    password_hash = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, password_hash=password_hash)
    return user_repo.save(new_user)
