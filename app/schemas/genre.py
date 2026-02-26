from pydantic import BaseModel
from typing import List

""" JSON structure for GET /genres/{id} endpoint"""


class GenreResponse(BaseModel):
    id: int
    name: str
    links: List[dict] = []

    class Config:
        from_attributes = True


""" JSON structure for GET /genres endpoint"""


class GenresListResponse(BaseModel):
    genres: List[GenreResponse]
    links: dict = {}
