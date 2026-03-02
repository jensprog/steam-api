from pydantic import BaseModel
from typing import List

""" JSON structure for GET /genres/{id} endpoint"""


class GenreResponse(BaseModel):
    id: int
    name: str
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


""" JSON structure for GET /genres endpoint"""


class GenresListResponse(BaseModel):
    genres: List[GenreResponse]
    pagination: PaginationResponse
    links: dict = {}
