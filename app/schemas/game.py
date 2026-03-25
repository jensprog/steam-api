from pydantic import BaseModel, field_validator
from typing import List, Optional
import html

"""
Pydantic models for game-related API request/response schemas.

Defines data validation and serialization models for game endpoints
including creation, updates, responses, and query parameters.
"""


class GameCreate(BaseModel):
    app_id: Optional[str] = None
    name: str
    price: float = 0.0
    release_date: Optional[str] = None
    short_description: Optional[str] = None
    windows: bool = False
    mac: bool = False
    linux: bool = False
    metacritic_score: int = 0
    positive: int = 0
    negative: int = 0

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, name_value):
        if name_value:
            return html.escape(name_value.strip())
        return name_value

    @field_validator("short_description")
    @classmethod
    def sanitize_description(cls, description_value):
        if description_value:
            return html.escape(description_value.strip())
        return description_value

    @field_validator("app_id")
    @classmethod
    def sanitize_app_id(cls, app_id_value):
        if app_id_value:
            return html.escape(app_id_value.strip())
        return app_id_value

    @field_validator("release_date")
    @classmethod
    def sanitize_release_date(cls, date_value):
        if date_value:
            return html.escape(date_value.strip())
        return date_value


""" JSON structure for GET /games/{id} endpoint"""


class GameResponse(BaseModel):
    id: int
    name: str
    price: float
    release_date: Optional[str] = None
    metacritic_score: int
    positive: int
    negative: int
    windows: bool
    mac: bool
    linux: bool
    average_playtime_forever: int
    estimated_owners: Optional[str] = None
    header_image: Optional[str] = None

    developers: List[str] = []
    genres: List[str] = []

    links: List[dict] = []

    class Config:
        from_attributes = True


""" JSON structure for GET /games endpoint with pagination"""


class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    has_next: bool
    has_previous: bool


""" JSON structure for GET /games endpoint with filtering and pagination"""


class GameQueryParameters(BaseModel):
    developer: Optional[str] = None
    genre: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 20


""" JSON structure for GET /games endpoint response with pagination and links"""


class GamesListResponse(BaseModel):
    games: List[GameResponse]
    pagination: PaginationResponse
    links: dict


""" JSON structure for PUT /games/{id} endpoint"""


class GameUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    release_date: Optional[str] = None
    short_description: Optional[str] = None
    windows: Optional[bool] = None
    mac: Optional[bool] = None
    linux: Optional[bool] = None
    metacritic_score: Optional[int] = None
    positive: Optional[int] = None
    negative: Optional[int] = None

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, name_value):
        if name_value:
            return html.escape(name_value.strip())
        return name_value

    @field_validator("short_description")
    @classmethod
    def sanitize_description(cls, description_value):
        if description_value:
            return html.escape(description_value.strip())
        return description_value

    @field_validator("release_date")
    @classmethod
    def sanitize_release_date(cls, date_value):
        if date_value:
            return html.escape(date_value.strip())
        return date_value
