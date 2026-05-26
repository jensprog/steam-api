from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.repositories.interfaces.stats_repository import StatsRepositoryInterface
from app.models.game import Game
from app.models.genre import Genre
from app.models.developer import Developer
from app.models import game_genres, game_developers
from app.schemas.developer import DeveloperQueryParameters
from typing import List, Tuple, Any


class SQLAlchemyStatsRepository(StatsRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def get_games_with_price(self) -> List[Any]:
        return self.db.query(Game.name, Game.price).filter(Game.price != None).all()  # noqa: E711

    def get_games_with_owners(self) -> List[Any]:
        return self.db.query(Game.name, Game.estimated_owners).filter(Game.estimated_owners != None).all()  # noqa: E711

    def get_genres_with_game_count(self) -> List[Any]:
        return (
            self.db.query(Genre.name, Genre.id, func.count(game_genres.c.game_id).label("game_count"))
            .join(game_genres)
            .group_by(Genre.name, Genre.id)
            .order_by(desc(func.count(game_genres.c.game_id)))
            .all()
        )

    def get_developers_with_game_count(self, params: DeveloperQueryParameters) -> Tuple[List[Any], int]:
        query = (
            self.db.query(Developer.name, Developer.id, func.count(game_developers.c.game_id).label("game_count"))
            .join(game_developers)
            .group_by(Developer.name, Developer.id)
            .order_by(desc(func.count(game_developers.c.game_id)))
        )

        total = self.db.query(func.count(Developer.id.distinct())).scalar()
        rows = query.limit(params.limit).offset((params.page - 1) * params.limit).all()

        return rows, total
