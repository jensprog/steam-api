from pydantic import BaseModel

"""
Pydantic models for game-related API request/response schemas.

Defines data validation and serialization models for game endpoints
including creation, updates, responses, and query parameters.
"""


class GameCreate(BaseModel):
    app_id: str | None = None
    name: str
    price: float = 0.0
    release_date: str | None = None
    short_description: str | None = None
    windows: bool = False
    mac: bool = False
    linux: bool = False
    developers: list[str] = []
    genres: list[str] = []


""" JSON structure for GET /games/{id} endpoint"""


class GameResponse(BaseModel):
    id: int
    name: str
    price: float
    release_date: str | None = None
    short_description: str | None = None
    metacritic_score: int
    positive: int
    negative: int
    windows: bool
    mac: bool
    linux: bool
    average_playtime_forever: int
    estimated_owners: str | None = None
    header_image: str | None = None

    developers: list[str] = []
    genres: list[str] = []

    links: list[dict] = []

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
    developer: str | None = None
    genre: str | None = None
    search: str | None = None
    page: int = 1
    limit: int = 20


""" JSON structure for GET /games endpoint response with pagination and links"""


class GamesListResponse(BaseModel):
    games: list[GameResponse]
    pagination: PaginationResponse
    links: dict


""" JSON structure for PUT /games/{id} endpoint"""


class GameUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    release_date: str | None = None
    short_description: str | None = None
    windows: bool | None = None
    mac: bool | None = None
    linux: bool | None = None
    developers: list[str] | None = None
    genres: list[str] | None = None
    metacritic_score: int | None = None
    positive: int | None = None
    negative: int | None = None


class RankingEntry(BaseModel):
    rank: int
    concurrent_in_game: int
    peak_in_game: int
    name: str
    header_image: str | None = None


class RankingsListResponse(BaseModel):
    rankings: list[RankingEntry]
    pagination: PaginationResponse
    links: dict


class RankQueryParameters(BaseModel):
    page: int = 1
    limit: int = 20
