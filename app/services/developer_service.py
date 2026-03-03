from sqlalchemy.orm import Session
from app.models.developer import Developer
from app.schemas import DeveloperResponse
from app.schemas.developer import DevelopersListResponse, PaginationResponse
from app.utils.serializers import serialize_developer
from app.utils.hateoasbuilder import build_pagination_links


def get_developers_list(db: Session, page: int = 1, limit: int = 20) -> DevelopersListResponse:
    developers = db.query(Developer).limit(limit).offset((page - 1) * limit).all()
    total_developers = db.query(Developer).count()

    developer_responses = [serialize_developer(developer) for developer in developers]

    pages = (total_developers + limit - 1) // limit
    pagination = PaginationResponse(
        page=page,
        limit=limit,
        total=total_developers,
        pages=pages,
        has_next=page < pages,
        has_previous=page > 1,
    )

    links = build_pagination_links("/developers", page, limit, pagination)

    return DevelopersListResponse(developers=developer_responses, pagination=pagination, links=links)


def get_developer_by_id(db: Session, developer_id: int) -> DeveloperResponse | None:
    developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if not developer:
        return None
    return serialize_developer(developer)
