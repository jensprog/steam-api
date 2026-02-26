from pydantic import BaseModel

""" JSON structure for user registration endpoint """


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
