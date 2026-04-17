from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.repositories.exceptions import ConstraintViolationError
from app.models.user import User


class SQLAlchemyUserRepository(UserRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def find_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def save(self, user: User) -> User:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise ConstraintViolationError("Username already exists. Please choose a different username.")
