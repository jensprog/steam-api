from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DeveloperResponse, DevelopersListResponse, DeveloperQueryParameters
from app.services.developer_service import get_developer_by_id, get_developers_list

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
    developer = get_developer_by_id(db, id)
    if not developer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found")
    return developer
