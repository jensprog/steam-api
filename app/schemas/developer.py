from pydantic import BaseModel
from app.schemas.game import PaginationResponse

"""
Pydantic models for developer-related API response schemas.

Defines read-only response models for developer endpoints.
"""


class DeveloperResponse(BaseModel):
    id: int
    name: str
    links: list[dict] = []

    class Config:
        from_attributes = True


class DeveloperQueryParameters(BaseModel):
    game: str | None = None
    genre: str | None = None
    search: str | None = None
    page: int = 1
    limit: int = 20


""" JSON structure for GET /developers endpoint"""


class DevelopersListResponse(BaseModel):
    developers: list[DeveloperResponse]
    pagination: PaginationResponse
    links: dict = {}


class DeveloperWithGameCount(BaseModel):
    name: str
    game_count: int
    id: int


class DevelopersWithGamesResponse(BaseModel):
    developers: list[DeveloperWithGameCount]
    pagination: PaginationResponse
    links: dict = {}
