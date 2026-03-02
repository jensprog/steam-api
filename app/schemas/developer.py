from pydantic import BaseModel
from typing import List

""" JSON structure for GET /developers/{id} endpoint"""


class DeveloperResponse(BaseModel):
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


""" JSON structure for GET /developers endpoint"""


class DevelopersListResponse(BaseModel):
    developers: List[DeveloperResponse]
    pagination: PaginationResponse
    links: dict = {}
