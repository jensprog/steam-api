from pydantic import BaseModel
from typing import List, Optional


class MovieData(BaseModel):
    thumbnail: str
    hls_h264: str
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