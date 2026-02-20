from pydantic import BaseModel
from typing import List, Optional


class GameCreate(BaseModel):
    app_id: Optional[str] = None
    name: str
    price: float = 0.0
    release_date: Optional[str] = None
    short_description: Optional[str] = None
    windows: bool = False
    mac: bool = False
    linux: bool = False
    metacritic_score: int = 0
    positive: int = 0
    negative: int = 0

    class GameResponse(BaseModel):
        id: int
        name: str
        price: float
        release_date: Optional[str] = None
        metacritic_score: int
        positive: int
        negative: int

        developers: List[str] = []
        genres: List[str] = []

        links: List[dict] = []

        class Config:
            from_attributes = True
