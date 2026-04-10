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
