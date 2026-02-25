from sqlalchemy.orm import Session
from app.models import Game, Developer, Genre
import pandas as pd
from typing import Dict


def load_developers(db: Session, developers: set) -> Dict[str, int]:
    """Load developers to database and returns a dictionary of developer names
    to their IDs."""
    print(f"Loading {len(developers)} developers into the database...")
    dev_map = {}

    for dev_name in developers:
        existing = db.query(Developer).filter(Developer.name == dev_name).first()

        if existing:
            dev_map[dev_name] = existing.id
        else:
            new_dev = Developer(name=dev_name)
            db.add(new_dev)
            db.flush()
            dev_map[dev_name] = new_dev.id

    db.commit()
    print(f"✅ Loaded {len(dev_map)} developers")
    return dev_map


def load_genres(db: Session, genres: set) -> Dict[str, int]:
    """Load genres to database and returns a dictionary of genre names to
    their IDs."""
    print(f"Loading {len(genres)} genres into the database...")
    genre_map = {}

    for genre_name in genres:
        existing = db.query(Genre).filter(Genre.name == genre_name).first()

        if existing:
            genre_map[genre_name] = existing.id
        else:
            new_genre = Genre(name=genre_name)
            db.add(new_genre)
            db.flush()
            genre_map[genre_name] = new_genre.id

    db.commit()
    print(f"✅ Loaded {len(genre_map)} genres")
    return genre_map


def load_games(db: Session, df: pd.DataFrame, dev_map: Dict[str, int], genre_map: Dict[str, int]):
    """Load games to database, linking to developers and genres."""
    print(f"Loading {len(df)} games into the database...")

    try:
        games_loaded = 0
        total_dev_links = 0
        total_genre_links = 0

        for _, row in df.iterrows():
            game = _create_game_from_row(row)
            total_dev_links += _link_developers_to_game(db, game, row, dev_map)
            total_genre_links += _link_genres_to_game(db, game, row, genre_map)

            db.add(game)
            games_loaded += 1

            if games_loaded % 100 == 0:
                print(f"Progress: {games_loaded}/{len(df)} games loaded...")

        db.commit()
        print(f"✅ Loaded all {games_loaded} games successfully!")
        print(f"Total developer links: {total_dev_links}")
        print(f"Total genre links: {total_genre_links}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error loading games: {e}")
        raise


def _create_game_from_row(row) -> Game:
    """Create Game object from DataFrame row."""
    return Game(
        app_id=str(row["app_id"]) if pd.notna(row["app_id"]) else "",
        name=str(row["name"]) if pd.notna(row["name"]) else "",
        release_date=str(row.get("release_date", "")),
        price=float(row["price"]) if pd.notna(row.get("price")) else 0.0,
        estimated_owners=str(row.get("estimated_owners", "")),
        metacritic_score=(
            int(row["metacritic_score"]) if pd.notna(row.get("metacritic_score")) else 0
        ),
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


def _link_developers_to_game(db: Session, game: Game, row, dev_map: Dict[str, int]) -> int:
    """Link developers to game. Returns number of links created."""
    dev_links_created = 0
    developers_data = row.get("developers")

    print(f"\nDEBUG Game '{game.name}':")
    print(f"  developers_data type: {type(developers_data)}")
    print(f" developers_data value: {developers_data}")

    if (
        developers_data is not None
        and isinstance(developers_data, list)
        and len(developers_data) > 0
    ):
        for dev_name in developers_data:
            print(f"  Looking for developer: '{dev_name}' (stripped: '{dev_name.strip()}')")
            print(f"  Is in dev_map? {dev_name.strip() in dev_map}")
            if dev_name and dev_name.strip() in dev_map:
                dev = db.query(Developer).filter(Developer.id == dev_map[dev_name.strip()]).first()
                print(f"  Found developer in DB: {dev}")
                if dev and dev not in game.developers:
                    game.developers.append(dev)
                    dev_links_created += 1
                    print(f" Appended developer to game '{game.name}'")

    return dev_links_created


def _link_genres_to_game(db: Session, game: Game, row, genre_map: Dict[str, int]) -> int:
    """Link genres to game. Returns number of links created."""
    genre_links_created = 0
    genres_data = row.get("genres")

    if genres_data is not None and isinstance(genres_data, list) and len(genres_data) > 0:
        for genre_name in genres_data:
            if genre_name and genre_name.strip() in genre_map:
                genre = db.query(Genre).filter(Genre.id == genre_map[genre_name.strip()]).first()
                if genre and genre not in game.genres:
                    game.genres.append(genre)
                    genre_links_created += 1

    return genre_links_created
