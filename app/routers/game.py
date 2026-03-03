from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
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


@router.get("/", response_model=GamesListResponse, status_code=200)
def get_games(
    params: GameQueryParameters = Depends(),
    db: Session = Depends(get_db),
) -> GamesListResponse:
    return get_games_list(db, params)


@router.get("/{id}", response_model=GameResponse, status_code=200)
def get_game(id: int, db: Session = Depends(get_db)) -> GameResponse:
    game = get_game_by_id(db, id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/", response_model=GameResponse, status_code=201)
def create_one_game(game_data: GameCreate, db: Session = Depends(get_db)) -> GameResponse:
    return create_game(db, game_data)


@router.put("/{id}", response_model=GameResponse, status_code=200)
def update_one_game(id: int, game_data: GameUpdate, db: Session = Depends(get_db)) -> GameResponse:
    updated_game = update_game(db, id, game_data)
    if not updated_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return updated_game


@router.delete("/{id}", status_code=204)
def delete_one_game(id: int, db: Session = Depends(get_db)):
    deleted = delete_game(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Game not found")
