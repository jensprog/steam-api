from pydantic import BaseModel
from typing import List, Optional
from app.schemas.game import PaginationResponse

"""
Pydantic models for genre-related API response schemas.

Defines read-only response models for genre endpoints.
"""


class GenreResponse(BaseModel):
    id: int
    name: str
    links: List[dict] = []

    class Config:
        from_attributes = True


class GenreQueryParameters(BaseModel):
    game: Optional[str] = None
    developer: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 20


""" JSON structure for GET /genres endpoint"""


class GenresListResponse(BaseModel):
    genres: List[GenreResponse]
    pagination: PaginationResponse
    links: dict = {}
