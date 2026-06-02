from pydantic import BaseModel
from app.schemas.game import PaginationResponse

"""
Pydantic models for genre-related API response schemas.

Defines read-only response models for genre endpoints.
"""


class GenreResponse(BaseModel):
    id: int
    name: str
    links: list[dict] = []

    class Config:
        from_attributes = True


class GenreQueryParameters(BaseModel):
    game: str | None = None
    developer: str | None = None
    search: str | None = None
    page: int = 1
    limit: int = 20


""" JSON structure for GET /genres endpoint"""


class GenresListResponse(BaseModel):
    genres: list[GenreResponse]
    pagination: PaginationResponse
    links: dict = {}


class GenreWithGameCount(BaseModel):
    name: str
    game_count: int
    id: int


class GenresWithGamesResponse(BaseModel):
    genres: list[GenreWithGameCount]


class GenreDetailResponse(BaseModel):
    name: str
    id: int
    links: list[dict] = []
    pagination: PaginationResponse
    pagination_links: dict = {}
