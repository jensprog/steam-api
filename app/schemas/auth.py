from pydantic import BaseModel, field_validator
from app.utils.validator import parse_username

"""
Pydantic models for authentication-related API schemas.

Defines request/response models for user registration, login,
and JWT token handling.
"""


class UserRegister(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username_value):
        return parse_username(username_value)


""" JSON structure for user login endpoint """


class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username_value):
        return parse_username(username_value)


""" JSON structure for token response """


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
