from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.models import Game, Developer, Genre
from app.models.game import game_developers, game_genres
import pandas as pd
from typing import Dict

BATCH_SIZE = 1000


def load_developers(db: Session, developers: set) -> Dict[str, int]:
    """Load developers to database using bulk insert and returns a dictionary
    of developer names to their IDs."""
    print(f"Loading {len(developers)} developers into the database...")

    dev_list = [{"name": name} for name in developers]
    statement = pg_insert(Developer).values(dev_list).on_conflict_do_nothing(index_elements=["name"])
    db.execute(statement)
    db.commit()

    all_devs = db.query(Developer.id, Developer.name).all()
    dev_map = {name: dev_id for dev_id, name in all_devs}
    print(f"Loaded {len(dev_map)} developers")
    return dev_map


def load_genres(db: Session, genres: set) -> Dict[str, int]:
    """Load genres to database using bulk insert and returns a dictionary
    of genre names to their IDs."""
    print(f"Loading {len(genres)} genres into the database...")

    genre_list = [{"name": name} for name in genres]
    statement = pg_insert(Genre).values(genre_list).on_conflict_do_nothing(index_elements=["name"])
    db.execute(statement)
    db.commit()

    all_genres = db.query(Genre.id, Genre.name).all()
    genre_map = {name: genre_id for genre_id, name in all_genres}
    print(f"Loaded {len(genre_map)} genres")
    return genre_map


def load_games(db: Session, df: pd.DataFrame, dev_map: Dict[str, int], genre_map: Dict[str, int]):
    """Load games to database in batches, linking to developers and genres
    via direct association table inserts."""
    print(f"Loading {len(df)} games into the database...")

    games_loaded = 0
    batch_games = []

    try:
        for _, row in df.iterrows():
            game = _create_game_from_row(row)
            db.add(game)
            batch_games.append((game, row))
            games_loaded += 1

            if games_loaded % BATCH_SIZE == 0:
                _flush_batch(db, batch_games, dev_map, genre_map)
                batch_games = []
                print(f"Progress: {games_loaded}/{len(df)} games loaded...")

        if batch_games:
            _flush_batch(db, batch_games, dev_map, genre_map)

        print(f"Loaded all {games_loaded} games successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error loading games: {e}")
        raise


def _create_game_from_row(row) -> Game:
    """Create Game object from DataFrame row."""
    return Game(
        app_id=str(row["app_id"]) if pd.notna(row["app_id"]) else "",
        name=str(row["name"]) if pd.notna(row["name"]) else "",
        release_date=str(row.get("release_date", "")),
        price=float(row["price"]) if pd.notna(row.get("price")) else 0.0,
        estimated_owners=str(row.get("estimated_owners", "")),
        metacritic_score=(int(row["metacritic_score"]) if pd.notna(row.get("metacritic_score")) else 0),
        positive=int(row["positive"]) if pd.notna(row.get("positive")) else 0,
        negative=int(row["negative"]) if pd.notna(row.get("negative")) else 0,
        average_playtime_forever=(
            int(
                float(row["average_playtime_forever"])
                if pd.notna(row.get("average_playtime_forever"))
                and str(row["average_playtime_forever"]).replace(".", "").isdigit()
                else 8
            )
        ),
        header_image=str(row.get("header_image", "")),
        windows=(bool(row.get("windows", False)) if pd.notna(row.get("windows")) else False),
        mac=bool(row.get("mac", False)) if pd.notna(row.get("mac")) else False,
        linux=(bool(row.get("linux", False)) if pd.notna(row.get("linux")) else False),
        short_description=str(row.get("short_description", "")),
    )


def _flush_batch(db: Session, batch_games: list, dev_map: Dict[str, int], genre_map: Dict[str, int]):
    """Flush a batch of games and insert their associations."""
    db.flush()

    dev_links = []
    genre_links = []

    for game, row in batch_games:
        devs_data = row.get("developers")
        if devs_data and isinstance(devs_data, list):
            for dev_name in devs_data:
                dev_name = dev_name.strip()
                if dev_name in dev_map:
                    dev_links.append({"game_id": game.id, "developer_id": dev_map[dev_name]})

        genres_data = row.get("genres")
        if genres_data and isinstance(genres_data, list):
            for genre_name in genres_data:
                genre_name = genre_name.strip()
                if genre_name in genre_map:
                    genre_links.append({"game_id": game.id, "genre_id": genre_map[genre_name]})

    if dev_links:
        statement = pg_insert(game_developers).values(dev_links).on_conflict_do_nothing()
        db.execute(statement)
    if genre_links:
        statement = pg_insert(game_genres).values(genre_links).on_conflict_do_nothing()
        db.execute(statement)

    db.commit()
