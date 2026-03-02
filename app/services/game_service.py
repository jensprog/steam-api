from sqlalchemy.orm import Session
from app.models.game import Game
from app.schemas import GamesListResponse, PaginationResponse
from app.schemas.game import GameCreate, GameResponse, GameUpdate
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


def get_game_by_id(db: Session, game_id: int) -> GameResponse | None:
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return None
    return serialize_game(game)


def create_game(db: Session, game_data: GameCreate) -> GameResponse:
    new_game = Game(**game_data.model_dump())
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return serialize_game(new_game)


def update_game(db: Session, game_id: int, game_data: GameUpdate) -> GameResponse | None:
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return None

    for key, value in game_data.model_dump(exclude_unset=True).items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return serialize_game(game)


def delete_game(db: Session, game_id: int) -> bool:
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return False

    db.delete(game)
    db.commit()
    return True
