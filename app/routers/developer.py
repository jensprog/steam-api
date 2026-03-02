from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DeveloperResponse, DevelopersListResponse
from app.services.developer_service import get_developers_list

""" Router for developer-related endpoints """

router = APIRouter(tags=["Developers"])


@router.get("/", response_model=DevelopersListResponse, status_code=200)
def get_developers(
    db: Session = Depends(get_db),
) -> DevelopersListResponse:
    developers = get_developers_list(db)
    return DevelopersListResponse(developers=developers, links={"self": "/developers"})
