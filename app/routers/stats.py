from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.interfaces.stats_repository import StatsRepositoryInterface
from app.repositories.sqlalchemy.stats_repository import SQLAlchemyStatsRepository
from app.repositories.interfaces.game_repository import GameRepositoryInterface
from app.repositories.sqlalchemy.game_repository import SQLAlchemyGameRepository
from app.schemas.developer import DeveloperQueryParameters
from app.schemas.game import RankQueryParameters
from app.services.steam_ranking_service import get_most_concurrent_games_played, get_all_ranks, concurrent_in_game
from app.services.stats_service import (
    get_games_by_amount_of_players,
    get_games_by_price,
    get_genres_with_game_count,
    get_developers_with_game_count,
)

router = APIRouter(tags=["Stats"])


def get_stats_repository(db: Session = Depends(get_db)) -> StatsRepositoryInterface:
    """Dependency injection for stats repository"""
    return SQLAlchemyStatsRepository(db)


def get_game_repository(db: Session = Depends(get_db)) -> GameRepositoryInterface:
    return SQLAlchemyGameRepository(db)


@router.get("/games/by-price", status_code=status.HTTP_200_OK)
def get_games_and_price(stats_repo: StatsRepositoryInterface = Depends(get_stats_repository)):
    return get_games_by_price(stats_repo)


@router.get("/games/by-owners", status_code=status.HTTP_200_OK)
def get_games_by_player_amount(stats_repo: StatsRepositoryInterface = Depends(get_stats_repository)):
    return get_games_by_amount_of_players(stats_repo)


@router.get("/genres/by-games", status_code=status.HTTP_200_OK)
def get_genres_by_games(stats_repo: StatsRepositoryInterface = Depends(get_stats_repository)):
    return get_genres_with_game_count(stats_repo)


@router.get("/developers/by-games", status_code=status.HTTP_200_OK)
def get_developers_by_games(
        params: DeveloperQueryParameters = Depends(),
        stats_repo: StatsRepositoryInterface = Depends(get_stats_repository)
):
    return get_developers_with_game_count(stats_repo, params)


@router.get("/games/concurrent-players", status_code=status.HTTP_200_OK)
def most_concurrent_players(game_repo: GameRepositoryInterface = Depends(get_game_repository)):
    return get_most_concurrent_games_played(game_repo)


@router.get("/games/all-concurrent-players", status_code=status.HTTP_200_OK)
def all_concurrent_players(
        params: RankQueryParameters = Depends(), game_repo: GameRepositoryInterface = Depends(get_game_repository)
):
    return get_all_ranks(game_repo, params)


@router.get("/games/concurrent-players-in-game", status_code=status.HTTP_200_OK)
def concurrent_players_in_game():
    return concurrent_in_game()
