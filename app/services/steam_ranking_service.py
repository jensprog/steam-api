# Logic for fetching most played games from ISteamChartsService
import requests
from app.core.config import settings
from app.repositories.interfaces.game_repository import GameRepositoryInterface


def get_most_concurrent_games_played(game_repo: GameRepositoryInterface):
    params = {"key": settings.STEAM_API_KEY}

    response = requests.get(
        "https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/", params=params
    )
    response.raise_for_status()
    data = response.json()

    top_games = data["response"]["ranks"][:10]
    result = []

    for entry in top_games:
        game = game_repo.find_by_app_id(entry["appid"])
        if game:
            result.append(
                {
                    "rank": entry["rank"],
                    "concurrent_in_game": entry["concurrent_in_game"],
                    "peak_in_game": entry["peak_in_game"],
                    "name": game.name,
                    "header_image": game.header_image,
                }
            )
    return result
