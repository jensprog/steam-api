from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.interfaces.developer_repository import DeveloperRepositoryInterface
from app.repositories.sqlalchemy.developer_repository import SQLAlchemyDeveloperRepository
from app.schemas import DeveloperResponse, DevelopersListResponse, DeveloperQueryParameters
from app.services.developer_service import get_developer_by_id, get_developers_list
from app.utils.errors import not_found_error, unproccessable_entity_error

"""
Router for developer-related endpoints.

Provides read-only access to developer information and their games.
"""

router = APIRouter(tags=["Developers"])


def get_developer_repository(db: Session = Depends(get_db)) -> DeveloperRepositoryInterface:
    """Dependency injection for developer repository"""
    return SQLAlchemyDeveloperRepository(db)


@router.get("", response_model=DevelopersListResponse, status_code=status.HTTP_200_OK)
def get_developers(
    params: DeveloperQueryParameters = Depends(),
    dev_repo: DeveloperRepositoryInterface = Depends(get_developer_repository),
) -> DevelopersListResponse:
    return get_developers_list(dev_repo, params)


@router.get("/{id}", response_model=DeveloperResponse, status_code=status.HTTP_200_OK)
def get_developer(
    id: int, dev_repo: DeveloperRepositoryInterface = Depends(get_developer_repository)
) -> DeveloperResponse:
    if id <= 0:
        raise unproccessable_entity_error("id", id, "ID must be a positive integer.")
    developer = get_developer_by_id(dev_repo, id)
    if not developer:
        raise not_found_error("developer", id)
    return developer
