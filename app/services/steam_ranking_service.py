# Logic for fetching most played games from ISteamChartsService
import requests
from app.core.config import settings
from app.repositories.interfaces.game_repository import GameRepositoryInterface
from app.schemas import RankingsListResponse, PaginationResponse
from app.schemas.game import RankQueryParameters
from app.utils.hateoasbuilder import build_pagination_links


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


def _fetch_all_ranks(game_repo: GameRepositoryInterface):
    params = {"key": settings.STEAM_API_KEY}

    response = requests.get(
        "https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/", params=params
    )

    response.raise_for_status()
    data = response.json()

    top_games = data["response"]["ranks"]
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
