from pydantic import BaseModel, field_validator
import html

"""
Pydantic models for authentication-related API schemas.

Defines request/response models for user registration, login,
and JWT token handling.
"""


class UserRegister(BaseModel):
    username: str
    password: str

    @field_validator('username')
    @classmethod
    def sanitize_username(cls, username_value):
        if username_value:
            return html.escape(username_value.strip())
        return username_value


""" JSON structure for user login endpoint """


class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator('username')
    @classmethod
    def sanitize_username(cls, username_value):
        if username_value:
            return html.escape(username_value.strip())
        return username_value


""" JSON structure for token response """


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
