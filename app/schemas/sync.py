# Pydantic schemas for validating and transforming game data from the Steam API appdetails endpoint.
from pydantic import BaseModel, field_validator, model_validator


class MovieData(BaseModel):
    thumbnail: str
    hls_h264: str | None = None
    name: str


class SteamAppData(BaseModel):
    app_id: str
    name: str
    price: float = 0.0
    release_date: str | None = None
    type: str | None = None
    short_description: str | None = None
    windows: bool = False
    mac: bool = False
    linux: bool = False
    developers: list[str] = []
    genres: list[str] = []
    header_image: str | None = None
    movies: list[MovieData] | None = None
    background: str | None = None
    recommendations: int | None = None
    screenshots: list[str] = []

    @model_validator(mode="before")
    @classmethod
    def parse_platforms(cls, v):
        if isinstance(v, dict) and "platforms" in v:
            platforms = v.get("platforms", {})
            v["windows"] = platforms.get("windows", False)
            v["mac"] = platforms.get("mac", False)
            v["linux"] = platforms.get("linux", False)
        return v

    @field_validator("recommendations", mode="before")
    @classmethod
    def parse_recommendations(cls, v):
        if isinstance(v, dict):
            return v.get("total")
        return v

    @field_validator("screenshots", mode="before")
    @classmethod
    def parse_screenshots(cls, v):
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return [s.get("path_full", "") for s in v]
        return v

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
