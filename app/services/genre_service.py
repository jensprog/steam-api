from sqlalchemy.orm import Session
from app.models.game import Game
from app.models.genre import Genre
from app.schemas.genre import GenreDetailResponse, GenresListResponse, PaginationResponse, GenreQueryParameters
from app.utils.serializers import serialize_genres
from app.utils.hateoasbuilder import build_pagination_links

"""
Business logic for genre operations.

Handles read-only genre operations with filtering and pagination.
"""


def get_genres_list(db: Session, params: GenreQueryParameters) -> GenresListResponse:
    query = db.query(Genre)
    if params.game:
        query = query.filter(Genre.games.any(name=params.game))
    if params.developer:
        query = query.filter(Genre.games.any(Game.developers.any(name=params.developer)))
    if params.search:
        query = query.filter(Genre.name.ilike(f"%{params.search}%"))

    total_genres = query.count()
    genres = query.limit(params.limit).offset((params.page - 1) * params.limit).all()

    genre_responses = [serialize_genres(genre, include_game_links=False) for genre in genres]

    pages = (total_genres + params.limit - 1) // params.limit
    pagination = PaginationResponse(
        page=params.page,
        limit=params.limit,
        total=total_genres,
        pages=pages,
        has_next=params.page < pages,
        has_previous=params.page > 1,
    )

    links = build_pagination_links("/genres", params.page, params.limit, pagination)

    return GenresListResponse(genres=genre_responses, pagination=pagination, links=links)


def get_genre_by_id(db: Session, genre_id: int, params: GenreQueryParameters) -> GenreDetailResponse | None:
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        return None

    games = db.query(Game).filter(Game.genres.any(id=genre.id))

    total_games = games.count()
    games = games.limit(params.limit).offset((params.page - 1) * params.limit).all()

    game_links = []
    for game in games:
        game_links.append(
            {"rel": "related", "href": f"/games/{game.id}", "method": "GET", "title": f"Game: {game.name}"}
        )

    pages = (total_games + params.limit - 1) // params.limit
    pagination = PaginationResponse(
        page=params.page,
        limit=params.limit,
        total=total_games,
        pages=pages,
        has_next=params.page < pages,
        has_previous=params.page > 1,
    )

    pagination_links = build_pagination_links(f"/genres/{genre_id}", params.page, params.limit, pagination)
    return GenreDetailResponse(
        id=genre.id, name=genre.name, links=game_links, pagination=pagination, pagination_links=pagination_links
    )
