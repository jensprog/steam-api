from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case, cast, Integer
from app.repositories.interfaces.stats_repository import StatsRepositoryInterface
from app.models.game import Game
from app.models.genre import Genre
from app.models.developer import Developer
from app.models import game_genres, game_developers
from app.schemas.developer import DeveloperQueryParameters
from typing import Any


class SQLAlchemyStatsRepository(StatsRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def get_price_distribution(self) -> list[tuple[str, int]]:
        row = self.db.query(
            func.sum(case((Game.price == 0, 1), else_=0)).label("free_na"),
            func.sum(case(((Game.price > 0) & (Game.price < 10), 1), else_=0)).label("under_10"),
            func.sum(case(((Game.price >= 10) & (Game.price <= 30), 1), else_=0)).label("ten_thirty"),
            func.sum(case((Game.price > 30, 1), else_=0)).label("over_30"),
        ).one()
        return [
            ("Free / NA", row.free_na or 0),
            ("Under $10", row.under_10 or 0),
            ("$10-30", row.ten_thirty or 0),
            ("Over $30", row.over_30 or 0),
        ]

    def get_owners_distribution(self) -> list[tuple[str, int]]:
        lower = cast(func.split_part(Game.estimated_owners, " - ", 1), Integer)
        row = (
            self.db.query(
                func.sum(case((lower == 0, 1), else_=0)).label("no_owners"),
                func.sum(case(((lower > 0) & (lower < 50000), 1), else_=0)).label("under_50k"),
                func.sum(case(((lower >= 50000) & (lower < 200000), 1), else_=0)).label("fifty_200k"),
                func.sum(case(((lower >= 200000) & (lower < 1000000), 1), else_=0)).label("between_200k_1m"),
                func.sum(case((lower >= 1000000, 1), else_=0)).label("over_1m"),
            )
            .filter(Game.estimated_owners is not None)
            .one()
        )  # noqa: E711
        return [
            ("No Owners / NA", row.no_owners or 0),
            ("Under 50k", row.under_50k or 0),
            ("50k-200k", row.fifty_200k or 0),
            ("200k-1M", row.between_200k_1m or 0),
            ("Over 1M", row.over_1m or 0),
        ]

    def get_genres_with_game_count(self) -> list[Any]:
        return (
            self.db.query(Genre.name, Genre.id, func.count(game_genres.c.game_id).label("game_count"))
            .join(game_genres)
            .group_by(Genre.name, Genre.id)
            .order_by(desc(func.count(game_genres.c.game_id)))
            .all()
        )

    def get_developers_with_game_count(self, params: DeveloperQueryParameters) -> tuple[list[Any], int]:
        query = (
            self.db.query(Developer.name, Developer.id, func.count(game_developers.c.game_id).label("game_count"))
            .join(game_developers)
            .group_by(Developer.name, Developer.id)
            .order_by(desc(func.count(game_developers.c.game_id)))
        )

        total = self.db.query(func.count(Developer.id.distinct())).scalar()
        rows = query.limit(params.limit).offset((params.page - 1) * params.limit).all()

        return rows, total
