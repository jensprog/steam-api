from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.schemas.auth import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token
from app.utils.errors import unauthorized_error

"""
User authentication service.

Handles user login and JWT token generation.
"""


def authenticate_user(user_repo: UserRepositoryInterface, login_data: UserLogin) -> TokenResponse:
    user = user_repo.find_by_username(login_data.username)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise unauthorized_error("Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token)
