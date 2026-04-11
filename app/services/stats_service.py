from sqlalchemy.orm import Session
from app.models import Game


def get_games_by_price(db: Session):
    games_with_price = db.query(Game.name, Game.price).filter(Game.price != None).all()  # noqa: E711
    price_sort_dict = {"Free": 0, "Under $10": 0, "$10-30": 0, "Over $30": 0}

    for price in games_with_price:
        if price.price == 0:
            price_sort_dict["Free"] += 1
        elif price.price > 0 and price.price < 10:
            price_sort_dict["Under $10"] += 1
        elif price.price >= 10 and price.price <= 30:
            price_sort_dict["$10-30"] += 1
        else:
            price_sort_dict["Over $30"] += 1
    return [{"name": n, "value": v} for n, v in price_sort_dict.items()]


def get_games_by_amount_of_players(db: Session):
    games_with_players = (
        db.query(Game.name, Game.estimated_owners).filter(Game.estimated_owners != None).all()  # noqa: E711
    )
    sort_estimated_players = {"No Owners": 0, "Under 50k": 0, "50k-200k": 0, "200k-1M": 0, "Over 1M": 0}

    for estimated_owners in games_with_players:
        lower = int(
            estimated_owners.estimated_owners.split(
                " - ",
            )[0]
        )

        if lower == 0:
            sort_estimated_players["No Owners"] += 1
        elif lower < 50000:
            sort_estimated_players["Under 50k"] += 1
        elif lower < 200000:
            sort_estimated_players["50k-200k"] += 1
        elif lower < 1000000:
            sort_estimated_players["200k-1M"] += 1
        else:
            sort_estimated_players["Over 1M"] += 1
    return [{"name": n, "value": v} for n, v in sort_estimated_players.items()]
