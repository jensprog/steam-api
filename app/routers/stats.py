from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.stats_service import get_games_by_price

router = APIRouter(tags=["Stats"])


@router.get("/games/by-price", status_code=status.HTTP_200_OK)
def get_games_and_price(db: Session = Depends(get_db)):
    return get_games_by_price(db)
