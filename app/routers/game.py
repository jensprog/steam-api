from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.interfaces import GameRepositoryInterface
from app.repositories.sqlalchemy_repositories import SQLAlchemyGameRepository
from app.schemas import GamesListResponse, GameResponse, GameCreate, GameUpdate, GameQueryParameters
from app.utils.errors import not_found_error, unproccessable_entity_error
from app.services.game_service import (
    create_game,
    delete_game,
    get_game_by_id,
    get_games_list,
    update_game,
)

"""
Router for game-related endpoints.

Handles all HTTP endpoints for game CRUD operations including
filterable listing, individual game retrieval, and authenticated
create/update/delete operations.
"""

router = APIRouter(tags=["Games"])


def get_game_repository(db: Session = Depends(get_db)) -> GameRepositoryInterface:
    """Dependency injection for game repository"""
    return SQLAlchemyGameRepository(db)


@router.get("/", response_model=GamesListResponse, status_code=status.HTTP_200_OK)
def get_games(
    params: GameQueryParameters = Depends(),
    game_repo: GameRepositoryInterface = Depends(get_game_repository),
) -> GamesListResponse:
    return get_games_list(game_repo, params)


@router.get("/{id}", response_model=GameResponse, status_code=status.HTTP_200_OK)
def get_game(id: int, game_repo: GameRepositoryInterface = Depends(get_game_repository)) -> GameResponse:
    if id <= 0:
        raise unproccessable_entity_error("id", id, "ID must be a positive integer.")
    game = get_game_by_id(game_repo, id)
    if not game:
        raise not_found_error("game", id)
    return game


@router.get("/{id}/price", status_code=status.HTTP_200_OK)
def get_game_price(id: int, game_repo: GameRepositoryInterface = Depends(get_game_repository)):
    if id <= 0:
        raise unproccessable_entity_error("id", id, "ID must be a positive integer.")
    game = get_game_by_id(game_repo, id)
    if not game:
        raise not_found_error("game", id)
    return {"price": game.price}


@router.post("/", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_one_game(
    game_data: GameCreate,
    game_repo: GameRepositoryInterface = Depends(get_game_repository),
    _current_user: User = Depends(get_current_user),
) -> GameResponse:
    return create_game(game_repo, game_data)


@router.put("/{id}", response_model=GameResponse, status_code=status.HTTP_200_OK)
def update_one_game(
    id: int,
    game_data: GameUpdate,
    game_repo: GameRepositoryInterface = Depends(get_game_repository),
    _current_user: User = Depends(get_current_user),
) -> GameResponse:
    if id <= 0:
        raise unproccessable_entity_error("id", id, "ID must be a positive integer.")
    updated_game = update_game(game_repo, id, game_data)
    if not updated_game:
        raise not_found_error("game", id)
    return updated_game


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_game(
    id: int,
    game_repo: GameRepositoryInterface = Depends(get_game_repository),
    _current_user: User = Depends(get_current_user),
):
    if id <= 0:
        raise unproccessable_entity_error("id", id, "ID must be a positive integer.")
    deleted = delete_game(game_repo, id)
    if not deleted:
        raise not_found_error("game", id)
