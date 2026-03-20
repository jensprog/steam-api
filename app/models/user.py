from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

"""
User model for authentication in the Steam Games API.

Defines the User entity for JWT-based authentication system.
"""


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
