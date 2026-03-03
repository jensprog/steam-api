from sqlalchemy.orm import Session
from app.models.game import Game
from app.schemas import GamesListResponse, PaginationResponse
from app.schemas.game import GameCreate, GameQueryParameters, GameResponse, GameUpdate
from app.utils.serializers import serialize_game
from app.utils.hateoasbuilder import build_pagination_links


def get_games_list(db: Session, params: GameQueryParameters) -> GamesListResponse:
    query = db.query(Game)
    if params.developer:
        query = query.filter(Game.developers.any(name=params.developer))
    if params.genre:
        query = query.filter(Game.genres.any(name=params.genre))

    games = query.limit(params.limit).offset((params.page - 1) * params.limit).all()
    total_games = query.count()

    game_responses = [serialize_game(game) for game in games]

    pages = (total_games + params.limit - 1) // params.limit
    pagination = PaginationResponse(
        page=params.page,
        limit=params.limit,
        total=total_games,
        pages=pages,
        has_next=params.page < pages,
        has_previous=params.page > 1,
    )

    links = build_pagination_links("/games", params.page, params.limit, pagination)

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
