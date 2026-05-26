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
    games_with_price = stats_repo.get_games_with_price()
    price_sort_dict = {"Free / NA": 0, "Under $10": 0, "$10-30": 0, "Over $30": 0}

    for price in games_with_price:
        if price.price == 0:
            price_sort_dict["Free / NA"] += 1
        elif price.price > 0 and price.price < 10:
            price_sort_dict["Under $10"] += 1
        elif price.price >= 10 and price.price <= 30:
            price_sort_dict["$10-30"] += 1
        else:
            price_sort_dict["Over $30"] += 1
    return [{"name": n, "value": v} for n, v in price_sort_dict.items()]


""" Fetches games and the estimated amount of owners for all the games
visualized in the frontend application in a bar chart """


def get_games_by_amount_of_players(stats_repo: StatsRepositoryInterface):
    games_with_players = stats_repo.get_games_with_owners()
    sort_estimated_players = {"No Owners / NA": 0, "Under 50k": 0, "50k-200k": 0, "200k-1M": 0, "Over 1M": 0}

    for estimated_owners in games_with_players:
        lower = int(
            estimated_owners.estimated_owners.split(
                " - ",
            )[0]
        )

        if lower == 0:
            sort_estimated_players["No Owners / NA"] += 1
        elif lower < 50000:
            sort_estimated_players["Under 50k"] += 1
        elif lower < 200000:
            sort_estimated_players["50k-200k"] += 1
        elif lower < 1000000:
            sort_estimated_players["200k-1M"] += 1
        else:
            sort_estimated_players["Over 1M"] += 1
    return [{"name": n, "value": v} for n, v in sort_estimated_players.items()]


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
