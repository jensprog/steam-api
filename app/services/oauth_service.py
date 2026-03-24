from sqlalchemy.orm import Session
from authlib.integrations.requests_client import OAuth2Session
import requests
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.core.security import create_access_token
from app.core.config import settings
from app.utils.errors import unauthorized_error

"""
OAuth authentication service.

Handles Google OAuth flow and user authentication via OAuth providers.
"""


def get_google_oauth_url() -> str:
    """Generate Google OAuth authorization URL."""
    client = OAuth2Session(
        settings.GOOGLE_CLIENT_ID, redirect_uri=settings.GOOGLE_REDIRECT_URI, scope=["openid", "email", "profile"]
    )
    authorization_url, _ = client.create_authorization_url("https://accounts.google.com/o/oauth2/auth")
    return authorization_url


def handle_google_callback(db: Session, code: str) -> TokenResponse:
    """Handle Google OAuth callback and create/login user."""
    # Exchange authorization code for access token
    client = OAuth2Session(settings.GOOGLE_CLIENT_ID, redirect_uri=settings.GOOGLE_REDIRECT_URI)

    token = client.fetch_token(
        "https://oauth2.googleapis.com/token", code=code, client_secret=settings.GOOGLE_CLIENT_SECRET
    )

    # Get user info from Google
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {token['access_token']}"}
    )

    if user_info_response.status_code != 200:
        raise unauthorized_error("Failed to get user info from Google")

    user_info = user_info_response.json()

    # Find or create user
    user = db.query(User).filter(User.email == user_info["email"]).first()

    if not user:
        # Create new user from Google profile
        username = user_info["email"].split("@")[0]
        # Ensure username is unique
        counter = 1
        original_username = username
        while db.query(User).filter(User.username == username).first():
            username = f"{original_username}{counter}"
            counter += 1

        user = User(
            username=username,
            email=user_info["email"],
            oauth_provider="google",
            oauth_id=user_info["id"],
            password_hash=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token)
