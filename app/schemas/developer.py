from pydantic import BaseModel
from typing import List

""" JSON structure for GET /developers/{id} endpoint"""


class DeveloperResponse(BaseModel):
    id: int
    name: str
    links: List[dict] = []

    class Config:
        from_attributes = True


""" JSON structure for GET /developers endpoint"""


class DevelopersListResponse(BaseModel):
    developers: List[DeveloperResponse]
    links: dict = {}
