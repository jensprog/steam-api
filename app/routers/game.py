from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas import GamesListResponse, GameResponse, GameCreate, GameUpdate, GameQueryParameters
from app.services.game_service import (
    create_game,
    delete_game,
    get_game_by_id,
    get_games_list,
    update_game,
)

""" Router for game-related endpoints """

router = APIRouter(tags=["Games"])


@router.get("/", response_model=GamesListResponse, status_code=status.HTTP_200_OK)
def get_games(
    params: GameQueryParameters = Depends(),
    db: Session = Depends(get_db),
) -> GamesListResponse:
    return get_games_list(db, params)


@router.get("/{id}", response_model=GameResponse, status_code=status.HTTP_200_OK)
def get_game(id: int, db: Session = Depends(get_db)) -> GameResponse:
    game = get_game_by_id(db, id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return game


@router.post("/", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_one_game(
    game_data: GameCreate, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)
) -> GameResponse:
    return create_game(db, game_data)


@router.put("/{id}", response_model=GameResponse, status_code=status.HTTP_200_OK)
def update_one_game(
    id: int, game_data: GameUpdate, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)
) -> GameResponse:
    updated_game = update_game(db, id, game_data)
    if not updated_game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return updated_game


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_game(id: int, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)):
    deleted = delete_game(db, id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
