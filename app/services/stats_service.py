from app.repositories.interfaces.stats_repository import StatsRepositoryInterface
from app.schemas import (
    GenreWithGameCount,
    GenresWithGamesResponse,
    DeveloperWithGameCount,
    DevelopersWithGamesResponse,
    DeveloperQueryParameters,
    PaginationResponse,
)
from app.utils.hateoasbuilder import build_pagination_links

""" Fetches games and their price to be sorted in a pie chart in the frontend application """


def get_games_by_price(stats_repo: StatsRepositoryInterface):
    return [{"name": name, "value": count} for name, count in stats_repo.get_price_distribution()]


""" Fetches games and the estimated amount of owners for all the games
visualized in the frontend application in a bar chart """


def get_games_by_amount_of_players(stats_repo: StatsRepositoryInterface):
    return [{"name": name, "value": count} for name, count in stats_repo.get_owners_distribution()]


""" Fetching genres with their game count """


def get_genres_with_game_count(stats_repo: StatsRepositoryInterface):
    genre_with_game_count = stats_repo.get_genres_with_game_count()

    genres_with_games = []

    for row in genre_with_game_count:
        genres_with_games.append(GenreWithGameCount(name=row.name, game_count=row.game_count, id=row.id))
    return GenresWithGamesResponse(genres=genres_with_games)


def get_developers_with_game_count(stats_repo: StatsRepositoryInterface, params: DeveloperQueryParameters):
    rows, total_developers_with_games = stats_repo.get_developers_with_game_count(params)

    pages = (total_developers_with_games + params.limit - 1) // params.limit
    pagination = PaginationResponse(
        page=params.page,
        limit=params.limit,
        total=total_developers_with_games,
        pages=pages,
        has_next=params.page < pages,
        has_previous=params.page > 1,
    )

    links = build_pagination_links("/developers/by-games", params.page, params.limit, pagination)

    developers_with_games = []

    for row in rows:
        developers_with_games.append(DeveloperWithGameCount(name=row.name, game_count=row.game_count, id=row.id))
    return DevelopersWithGamesResponse(developers=developers_with_games, pagination=pagination, links=links)
