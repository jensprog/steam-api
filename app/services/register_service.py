from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import get_password_hash
from app.utils.errors import validation_error

"""
User registration service.

Handles new user creation with password hashing and
duplicate username validation.
"""


def register_user(db: Session, user_data: UserRegister) -> User:
    password_hash = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, password_hash=password_hash)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise validation_error(
            "username", user_data.username, "Username already exists. Please choose a different username."
        )
