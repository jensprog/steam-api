from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import GamesListResponse
from app.services.game_service import get_games_list

""" Router for game-related endpoints """

router = APIRouter(tags=["Games"])


@router.get("/", response_model=GamesListResponse)
def get_games(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=1000, description="Number of items per page"),
    db: Session = Depends(get_db),
) -> GamesListResponse:
    return get_games_list(db, page=page, limit=limit)
