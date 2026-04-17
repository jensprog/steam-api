from fastapi import APIRouter, Depends, status, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.rate_limit import limiter
from app.core.security import create_access_token, get_current_user
from app.database import get_db
from app.repositories.exceptions import ConstraintViolationError
from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository
from app.schemas.auth import UserLogin, UserRegister, TokenResponse
from app.services.register_service import register_user
from app.services.login_service import authenticate_user
from app.services.oauth_service import get_google_oauth_url, handle_google_callback
from app.utils.errors import validation_error

"""
Router for authentication-related endpoints.

Provides user registration and login endpoints with JWT token generation.
"""

router = APIRouter(tags=["Authentication"])


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryInterface:
    """Dependency injection for user repository"""
    return SQLAlchemyUserRepository(db)


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(
    request: Request, user_data: UserRegister, user_repo: UserRepositoryInterface = Depends(get_user_repository)
):
    try:
        user = register_user(user_repo, user_data)
    except ConstraintViolationError:
        raise validation_error(
            "username", user_data.username, "Username already exists. Please choose a different username."
        )
    return {"message": "User registered successfully", "username": user.username}


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def login(
    request: Request, login_data: UserLogin, user_repo: UserRepositoryInterface = Depends(get_user_repository)
) -> TokenResponse:
    return authenticate_user(user_repo, login_data)


@router.get("/google")
def google_login():
    """Initiate Google OAuth login."""
    authorization_url = get_google_oauth_url()
    return RedirectResponse(url=authorization_url)


@router.get("/google/callback", response_model=TokenResponse)
def google_callback(code: str = Query(...), user_repo: UserRepositoryInterface = Depends(get_user_repository)):
    """Handle Google OAuth callback and return JWT token."""
    return handle_google_callback(user_repo, code)


@router.get("/me")
def get_current_user_info(current_user=Depends(get_current_user)):
    """Get current authenticated user's info."""
    return {"username": current_user.username, "email": current_user.email}


@router.get("/refresh")
def refresh_token(current_user=Depends(get_current_user)):
    """Refresh JWT token for authenticated user."""
    access_token = create_access_token(data={"sub": current_user.username})
    return TokenResponse(access_token=access_token)
