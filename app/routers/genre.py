from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.interfaces.genre_repository import GenreRepositoryInterface
from app.repositories.sqlalchemy.genre_repository import SQLAlchemyGenreRepository
from app.schemas import GenresListResponse, GenreQueryParameters
from app.schemas.genre import GenreDetailResponse
from app.services.genre_service import get_genre_by_id, get_genres_list
from app.utils.errors import not_found_error, unproccessable_entity_error

"""
Router for genre-related endpoints.

Provides read-only access to genre information and their games.
"""

router = APIRouter(tags=["Genres"])


def get_genre_repository(db: Session = Depends(get_db)) -> GenreRepositoryInterface:
    """Dependency injection for genre repository"""
    return SQLAlchemyGenreRepository(db)


@router.get("", response_model=GenresListResponse, status_code=status.HTTP_200_OK)
def get_genres(
    params: GenreQueryParameters = Depends(),
    genre_repo: GenreRepositoryInterface = Depends(get_genre_repository),
) -> GenresListResponse:
    return get_genres_list(genre_repo, params)


@router.get("/{id}", response_model=GenreDetailResponse, status_code=status.HTTP_200_OK)
def get_genre(
    id: int,
    genre_repo: GenreRepositoryInterface = Depends(get_genre_repository),
    params: GenreQueryParameters = Depends(),
) -> GenreDetailResponse:
    if id <= 0:
        raise unproccessable_entity_error("id", id, "ID must be a positive integer.")
    genre = get_genre_by_id(genre_repo, id, params)
    if not genre:
        raise not_found_error("genre", id)
    return genre
