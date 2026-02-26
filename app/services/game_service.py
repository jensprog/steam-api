from sqlalchemy.orm import Session
from app.models.game import Game
from app.schemas import GamesListResponse, PaginationResponse
from app.utils.serializers import serialize_game


def get_games_list(db: Session, page: int = 1, limit: int = 20) -> GamesListResponse:
    games = db.query(Game).limit(limit).offset((page - 1) * limit).all()
    total_games = db.query(Game).count()

    game_responses = [serialize_game(game) for game in games]

    pages = (total_games + limit - 1) // limit
    pagination = PaginationResponse(
        page=page,
        limit=limit,
        total=total_games,
        pages=pages,
        has_next=page < pages,
        has_previous=page > 1,
    )

    links = {"self": f"/games?page={page}&limit={limit}"}
    if pagination.has_next:
        links["next"] = f"/games?page={page + 1}&limit={limit}"
    if pagination.has_previous:
        links["previous"] = f"/games?page={page - 1}&limit={limit}"

    return GamesListResponse(games=game_responses, pagination=pagination, links=links)
