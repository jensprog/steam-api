from pydantic import BaseModel
from typing import List, Optional
from app.schemas.game import PaginationResponse

"""
Pydantic models for developer-related API response schemas.

Defines read-only response models for developer endpoints.
"""


class DeveloperResponse(BaseModel):
    id: int
    name: str
    links: List[dict] = []

    class Config:
        from_attributes = True


class DeveloperQueryParameters(BaseModel):
    game: Optional[str] = None
    genre: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 20


""" JSON structure for GET /developers endpoint"""


class DevelopersListResponse(BaseModel):
    developers: List[DeveloperResponse]
    pagination: PaginationResponse
    links: dict = {}


class DeveloperWithGameCount(BaseModel):
    name: str
    game_count: int


class DevelopersWithGamesResponse(BaseModel):
    developers: List[DeveloperWithGameCount]
