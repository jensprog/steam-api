from pydantic import BaseModel

"""
Pydantic models for authentication-related API schemas.

Defines request/response models for user registration, login,
and JWT token handling.
"""


class UserRegister(BaseModel):
    username: str
    password: str


""" JSON structure for user login endpoint """


class UserLogin(BaseModel):
    username: str
    password: str


""" JSON structure for token response """


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
