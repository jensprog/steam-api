from sqlalchemy.orm import Session
from app.models.genre import Genre
from app.schemas import GenreResponse
from app.schemas.genre import GenresListResponse, PaginationResponse
from app.utils.serializers import serialize_genres
from app.utils.hateoasbuilder import build_pagination_links


def get_genres_list(db: Session, page: int = 1, limit: int = 20) -> GenresListResponse:
    genres = db.query(Genre).limit(limit).offset((page - 1) * limit).all()
    total_genres = db.query(Genre).count()

    genre_responses = [serialize_genres(genre) for genre in genres]

    pages = (total_genres + limit - 1) // limit
    pagination = PaginationResponse(
        page=page,
        limit=limit,
        total=total_genres,
        pages=pages,
        has_next=page < pages,
        has_previous=page > 1,
    )

    links = build_pagination_links("/genres", page, limit, pagination)

    return GenresListResponse(genres=genre_responses, pagination=pagination, links=links)


def get_genre_by_id(db: Session, genre_id: int) -> GenreResponse | None:
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        return None
    return serialize_genres(genre)
