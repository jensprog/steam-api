# Pydantic schemas for validating and transforming game data from the Steam API appdetails endpoint.
from pydantic import BaseModel, field_validator
from typing import List, Optional


class MovieData(BaseModel):
    thumbnail: str
    hls_h264: Optional[str] = None
    name: str


class SteamAppData(BaseModel):
    app_id: str
    name: str
    price: float = 0.0
    release_date: Optional[str] = None
    short_description: Optional[str] = None
    windows: bool = False
    mac: bool = False
    linux: bool = False
    developers: List[str] = []
    genres: List[str] = []
    movies: Optional[List[MovieData]] = []

    @field_validator("release_date", mode="before")
    @classmethod
    def parse_release_date(cls, v):
        if isinstance(v, dict):
            return v.get("date")
        return v

    @field_validator("genres", mode="before")
    @classmethod
    def parse_genres(cls, v):
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return [g.get("description", "") for g in v]
        return v
