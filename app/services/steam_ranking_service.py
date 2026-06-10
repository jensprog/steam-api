# Logic for fetching most played games from ISteamChartsService
import time
import requests
from app.core.config import settings
from app.repositories.interfaces.game_repository import GameRepositoryInterface
from app.schemas import RankingsListResponse, PaginationResponse
from app.schemas.game import RankQueryParameters, RankingEntry
from app.utils.hateoasbuilder import build_pagination_links

_steam_cache: dict = {"ranks": None, "timestamp": 0.0}
_CACHE_TTL = 300  # seconds


def get_most_concurrent_games_played(game_repo: GameRepositoryInterface):
    top_10_games = _fetch_all_ranks(game_repo)[:10]
    return top_10_games


def get_all_ranks(game_repo: GameRepositoryInterface, params: RankQueryParameters) -> RankingsListResponse:
    all_ranks = _fetch_all_ranks(game_repo)
    total = len(all_ranks)

    pages = (total + params.limit - 1) // params.limit
    pagination = PaginationResponse(
        page=params.page,
        limit=params.limit,
        total=total,
        pages=pages,
        has_next=params.page < pages,
        has_previous=params.page > 1,
    )

    links = build_pagination_links("/rankings", params.page, params.limit, pagination)

    offset = (params.page - 1) * params.limit
    paginated = all_ranks[offset : offset + params.limit]
    return RankingsListResponse(rankings=paginated, pagination=pagination, links=links)


def concurrent_in_game():
    total_players_in_game = _get_steam_ranks()
    count = 0

    for entry in total_players_in_game:
        count += entry["concurrent_in_game"]

    return count


def _fetch_all_ranks(game_repo: GameRepositoryInterface):
    raw_ranks = _get_steam_ranks()

    app_ids = [entry["appid"] for entry in raw_ranks]
    games = game_repo.find_by_app_ids(app_ids)
    game_map = {game.app_id: game for game in games}

    return [
        RankingEntry(
            rank=entry["rank"],
            concurrent_in_game=entry["concurrent_in_game"],
            peak_in_game=entry["peak_in_game"],
            name=game_map[entry["appid"]].name,
            header_image=game_map[entry["appid"]].header_image,
        )
        for entry in raw_ranks
        if entry["appid"] in game_map
    ]


def _get_steam_ranks() -> list:
    now = time.monotonic()
    if _steam_cache["ranks"] is not None and now - _steam_cache["timestamp"] < _CACHE_TTL:
        return _steam_cache["ranks"]

    response = requests.get(
        "https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/",
        params={"key": settings.STEAM_API_KEY},
    )
    response.raise_for_status()

    ranks = response.json()["response"]["ranks"]
    _steam_cache["ranks"] = ranks
    _steam_cache["timestamp"] = now
    return ranks
