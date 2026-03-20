from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserLogin, UserRegister, TokenResponse
from app.services.register_service import register_user
from app.services.login_service import authenticate_user

"""
Router for authentication-related endpoints.

Provides user registration and login endpoints with JWT token generation.
"""

router = APIRouter(tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    return {"message": "User registered successfully", "username": user.username}


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(login_data: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    return authenticate_user(db, login_data)
