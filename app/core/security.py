from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.config import settings
from app.utils.errors import unauthorized_error

"""
Security utilities for JWT authentication and password handling.

This module provides JWT token creation/verification, password hashing,
and FastAPI dependency for user authentication.
"""

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.PyJWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise unauthorized_error("Invalid authentication credentials")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise unauthorized_error("User not found")
    return user
