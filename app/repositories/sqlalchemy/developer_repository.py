from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.repositories.interfaces.developer_repository import DeveloperRepositoryInterface
from app.models.game import Game
from app.models.developer import Developer
from app.schemas.developer import DeveloperQueryParameters

"""
SQLAlchemy implementation of developer repository interface.

Handles database operations for developer GET operations including filtering
"""


class SQLAlchemyDeveloperRepository(DeveloperRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, developer_id: int) -> Optional[Developer]:
        return self.db.query(Developer).filter(Developer.id == developer_id).first()

    def find_filtered(self, params: DeveloperQueryParameters) -> Tuple[List[Developer], int]:
        query = self.db.query(Developer)

        if params.search:
            query = query.filter(Developer.name.ilike(f"%{params.search}%"))
        if params.game:
            query = query.filter(Developer.games.any(name=params.game))
        if params.genre:
            query = query.filter(Developer.games.any(Game.genres.any(name=params.genre)))

        total_developers = query.count()
        developers = query.limit(params.limit).offset((params.page - 1) * params.limit).all()

        return developers, total_developers
