from app.models.game import Game
from app.schemas import GameResponse

""" Utility functions for serializing database models into API response schemas """


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
        game_dict["links"] = [
            {"rel": "self", "href": f"/games/{game.id}", "method": "GET"},
            {"rel": "update", "href": f"/games/{game.id}", "method": "PUT"},
            {"rel": "delete", "href": f"/games/{game.id}", "method": "DELETE"},
        ]

    return GameResponse(**game_dict)
