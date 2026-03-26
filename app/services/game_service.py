from app.repositories.interfaces import GameRepositoryInterface, RepositoryError
from app.schemas import GamesListResponse, PaginationResponse
from app.schemas.game import GameCreate, GameQueryParameters, GameResponse, GameUpdate
from app.utils.serializers import serialize_game
from app.utils.hateoasbuilder import build_pagination_links
from app.utils.errors import validation_error, forbidden_error

"""
Business logic for game operations.

Handles game CRUD operations with proper serialization,
pagination, and error handling.
"""


def get_games_list(game_repo: GameRepositoryInterface, params: GameQueryParameters) -> GamesListResponse:
    games, total_games = game_repo.find_filtered(params)

    game_responses = [serialize_game(game) for game in games]

    pages = (total_games + params.limit - 1) // params.limit
    pagination = PaginationResponse(
        page=params.page,
        limit=params.limit,
        total=total_games,
        pages=pages,
        has_next=params.page < pages,
        has_previous=params.page > 1,
    )

    links = build_pagination_links("/games", params.page, params.limit, pagination)

    return GamesListResponse(games=game_responses, pagination=pagination, links=links)


def get_game_by_id(game_repo: GameRepositoryInterface, game_id: int) -> GameResponse | None:
    game = game_repo.find_by_id(game_id)
    if not game:
        return None
    return serialize_game(game)


def create_game(game_repo: GameRepositoryInterface, game_data: GameCreate, owner_id: int) -> GameResponse:
    try:
        new_game = game_repo.save(game_data, owner_id)
        return serialize_game(new_game)
    except RepositoryError as e:
        raise validation_error("game", game_data, str(e))


def update_game(
    game_repo: GameRepositoryInterface, game_id: int, game_data: GameUpdate, owner_id: int
) -> GameResponse | None:
    existing_game = game_repo.find_by_id(game_id)
    if not existing_game:
        return None
    if existing_game.owner_id is not None and existing_game.owner_id != owner_id:
        raise forbidden_error("You do not have permission to update this game.")
    try:
        game = game_repo.update(game_id, game_data)
        if not game:
            return None
        return serialize_game(game)
    except RepositoryError as e:
        raise validation_error("game", game_data, str(e))


def delete_game(game_repo: GameRepositoryInterface, game_id: int, owner_id: int) -> bool:
    existing_game = game_repo.find_by_id(game_id)
    if not existing_game:
        return False
    if existing_game.owner_id is not None and existing_game.owner_id != owner_id:
        raise forbidden_error("You do not have permission to delete this game.")
    try:
        return game_repo.remove(game_id)
    except RepositoryError as e:
        raise validation_error("game_id", game_id, str(e))
