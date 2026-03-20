from sqlalchemy.orm import Session
from app.models.developer import Developer
from app.models.game import Game
from app.schemas import DeveloperResponse
from app.schemas.developer import DevelopersListResponse, PaginationResponse, DeveloperQueryParameters
from app.utils.serializers import serialize_developer
from app.utils.hateoasbuilder import build_pagination_links

"""
Business logic for developer operations.

Handles read-only developer operations with filtering and pagination.
"""


def get_developers_list(db: Session, params: DeveloperQueryParameters) -> DevelopersListResponse:
    query = db.query(Developer)
    if params.search:
        query = query.filter(Developer.name.ilike(f"%{params.search}%"))
    if params.game:
        query = query.filter(Developer.games.any(name=params.game))
    if params.genre:
        query = query.filter(Developer.games.any(Game.genres.any(name=params.genre)))

    total_developers = query.count()
    developers = query.limit(params.limit).offset((params.page - 1) * params.limit).all()

    developer_responses = [serialize_developer(developer) for developer in developers]

    pages = (total_developers + params.limit - 1) // params.limit
    pagination = PaginationResponse(
        page=params.page,
        limit=params.limit,
        total=total_developers,
        pages=pages,
        has_next=params.page < pages,
        has_previous=params.page > 1,
    )

    links = build_pagination_links("/developers", params.page, params.limit, pagination)

    return DevelopersListResponse(developers=developer_responses, pagination=pagination, links=links)


def get_developer_by_id(db: Session, developer_id: int) -> DeveloperResponse | None:
    developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if not developer:
        return None
    return serialize_developer(developer)
