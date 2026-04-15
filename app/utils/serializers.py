from app.models.developer import Developer
from app.models.game import Game
from app.models.genre import Genre
from app.schemas import GameResponse, DeveloperResponse
from app.schemas.genre import GenreResponse
from app.utils.hateoasbuilder import build_resource_links

"""
Utility functions for serializing database models into API response schemas.

Converts SQLAlchemy models to Pydantic response models with optional
HATEOAS links for resource navigation.
"""


def serialize_game(game: Game, include_links: bool = True) -> GameResponse:
    game_dict = {
        "id": game.id,
        "name": game.name,
        "price": game.price or 0.0,
        "release_date": game.release_date,
        "metacritic_score": game.metacritic_score or 0,
        "positive": game.positive or 0,
        "negative": game.negative or 0,
        "windows": game.windows,
        "mac": game.mac,
        "linux": game.linux,
        "average_playtime_forever": game.average_playtime_forever or 0,
        "estimated_owners": game.estimated_owners,
        "header_image": game.header_image,
        "developers": [dev.name for dev in game.developers],
        "genres": [genre.name for genre in game.genres],
        "links": [],
    }

    if include_links:
        game_dict["links"] = build_resource_links("games", game.id, include_crud=True)

        for dev in game.developers:
            game_dict["links"].append(
                {"rel": "related", "href": f"/developers/{dev.id}", "method": "GET", "title": f"Developer: {dev.name}"}
            )

        for genre in game.genres:
            game_dict["links"].append(
                {"rel": "related", "href": f"/genres/{genre.id}", "method": "GET", "title": f"Genre: {genre.name}"}
            )

    return GameResponse(**game_dict)


def serialize_developer(developer: Developer, include_links: bool = True) -> DeveloperResponse:
    developer_dict = {
        "id": developer.id,
        "name": developer.name,
        "links": [],
    }

    if include_links:
        developer_dict["links"] = build_resource_links("developers", developer.id, include_crud=False)

        for game in developer.games:
            developer_dict["links"].append(
                {"rel": "related", "href": f"/games/{game.id}", "method": "GET", "title": f"Game: {game.name}"}
            )

    return DeveloperResponse(**developer_dict)


def serialize_genres(genres: Genre, include_links: bool = True, include_game_links: bool = True) -> GenreResponse:
    genre_dict = {
        "id": genres.id,
        "name": genres.name,
        "links": [],
    }

    if include_links:
        genre_dict["links"] = build_resource_links("genres", genres.id, include_crud=False)

        if include_game_links:
            for game in genres.games:
                genre_dict["links"].append(
                    {"rel": "related", "href": f"/games/{game.id}", "method": "GET", "title": f"Game: {game.name}"}
                )

    return GenreResponse(**genre_dict)
