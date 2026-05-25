from app.repositories.interfaces.genre_repository import GenreRepositoryInterface
from app.schemas.genre import GenreDetailResponse, GenresListResponse, PaginationResponse, GenreQueryParameters
from app.utils.serializers import serialize_genres
from app.utils.hateoasbuilder import build_pagination_links

"""
Business logic for genre operations.

Handles read-only genre operations with filtering and pagination.
"""


def get_genres_list(genre_repo: GenreRepositoryInterface, params: GenreQueryParameters) -> GenresListResponse:
    genres, total_genres = genre_repo.find_filtered(params)

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


def get_genre_by_id(
    genre_repo: GenreRepositoryInterface, genre_id: int, params: GenreQueryParameters
) -> GenreDetailResponse | None:

    genre = genre_repo.find_by_id(genre_id)
    if not genre:
        return None

    games, total_games = genre_repo.find_games_by_genre(genre_id, params)

    game_links = []
    for game in games:
        game_links.append(
            {
                "rel": "related",
                "href": f"/games/{game.id}",
                "method": "GET",
                "title": f"Game: {game.name}",
                "header_image": game.header_image,
            }
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
