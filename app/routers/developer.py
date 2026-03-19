from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DeveloperResponse, DevelopersListResponse, DeveloperQueryParameters
from app.services.developer_service import get_developer_by_id, get_developers_list
from app.utils.errors import not_found_error, unproccessable_entity_error

""" Router for developer-related endpoints """

router = APIRouter(tags=["Developers"])


@router.get("/", response_model=DevelopersListResponse, status_code=status.HTTP_200_OK)
def get_developers(
    params: DeveloperQueryParameters = Depends(),
    db: Session = Depends(get_db),
) -> DevelopersListResponse:
    return get_developers_list(db, params)


@router.get("/{id}", response_model=DeveloperResponse, status_code=status.HTTP_200_OK)
def get_developer(id: int, db: Session = Depends(get_db)) -> DeveloperResponse:
    if id <= 0:
        raise unproccessable_entity_error("id", id, "ID must be a positive integer.")
    developer = get_developer_by_id(db, id)
    if not developer:
        raise not_found_error("developer", id)
    return developer
