from .game import (
    GameCreate,
    GameResponse,
    GameUpdate,
    GamesListResponse,
    PaginationResponse,
    GameQueryParameters,
)
from .developer import (
    DeveloperResponse,
    DevelopersListResponse,
    DeveloperQueryParameters,
    DeveloperWithGameCount,
    DevelopersWithGamesResponse,
)
from .genre import GenreResponse, GenresListResponse, GenreQueryParameters, GenreWithGameCount, GenresWithGamesResponse
from .auth import UserRegister, UserLogin, TokenResponse

__all__ = [
    "GameCreate",
    "GameResponse",
    "GameUpdate",
    "GamesListResponse",
    "PaginationResponse",
    "GameQueryParameters",
    "DeveloperResponse",
    "DevelopersListResponse",
    "DeveloperQueryParameters",
    "DeveloperWithGameCount",
    "DevelopersWithGamesResponse",
    "GenreResponse",
    "GenresListResponse",
    "GenreQueryParameters",
    "GenreWithGameCount",
    "GenresWithGamesResponse",
    "UserRegister",
    "UserLogin",
    "TokenResponse",
]
