from pydantic import BaseModel
from typing import List, Optional

""" JSON structure for POST /games endpoint"""


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


""" JSON structure for GET /games/{id} endpoint"""


class GameResponse(BaseModel):
    id: int
    name: str
    price: float
    release_date: Optional[str] = None
    metacritic_score: int
    positive: int
    negative: int

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
