from pydantic_settings import BaseSettings

"""
Configuration management for the Steam Games API.

This module defines application settings using Pydantic BaseSettings
for environment variable management and validation.
"""


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
