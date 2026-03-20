from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token
from app.utils.errors import unauthorized_error

"""
User authentication service.

Handles user login and JWT token generation.
"""


def authenticate_user(db: Session, login_data: UserLogin) -> TokenResponse:
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise unauthorized_error("Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token)
