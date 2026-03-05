from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import GenreResponse, GenresListResponse
from app.services.genre_service import get_genre_by_id, get_genres_list

""" Router for genre-related endpoints """

router = APIRouter(tags=["Genres"])


@router.get("/", response_model=GenresListResponse, status_code=status.HTTP_200_OK)
def get_genres(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=1000, description="Number of items per page"),
    db: Session = Depends(get_db),
) -> GenresListResponse:
    return get_genres_list(db, page=page, limit=limit)


@router.get("/{id}", response_model=GenreResponse, status_code=status.HTTP_200_OK)
def get_genre(id: int, db: Session = Depends(get_db)) -> GenreResponse:
    genre = get_genre_by_id(db, id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return genre
