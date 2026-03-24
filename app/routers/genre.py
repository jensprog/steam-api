from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import GenreResponse, GenresListResponse, GenreQueryParameters
from app.services.genre_service import get_genre_by_id, get_genres_list
from app.utils.errors import not_found_error, unproccessable_entity_error

"""
Router for genre-related endpoints.

Provides read-only access to genre information and their games.
"""

router = APIRouter(tags=["Genres"])


@router.get("", response_model=GenresListResponse, status_code=status.HTTP_200_OK)
def get_genres(
    params: GenreQueryParameters = Depends(),
    db: Session = Depends(get_db),
) -> GenresListResponse:
    return get_genres_list(db, params)


@router.get("/{id}", response_model=GenreResponse, status_code=status.HTTP_200_OK)
def get_genre(id: int, db: Session = Depends(get_db)) -> GenreResponse:
    if id <= 0:
        raise unproccessable_entity_error("id", id, "ID must be a positive integer.")
    genre = get_genre_by_id(db, id)
    if not genre:
        raise not_found_error("genre", id)
    return genre
