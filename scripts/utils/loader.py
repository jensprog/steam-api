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
    games_loaded = 0

    for idx, row in df.iterrows():

        game = Game(
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

        if pd.notna(row.get("Developers")):
            dev_names = [d.strip() for d in str(row["Developers"]).split(",")]
            for dev_name in dev_names:
                if dev_name in dev_map:
                    dev = db.query(Developer).filter(Developer.id == dev_map[dev_name]).first()
                    if dev:
                        game.developers.append(dev)

        if pd.notna(row.get("Genres")):
            genre_names = [g.strip() for g in str(row["Genres"]).split(",")]
            for genre_name in genre_names:
                if genre_name in genre_map:
                    genre = db.query(Genre).filter(Genre.id == genre_map[genre_name]).first()
                    if genre:
                        game.genres.append(genre)

        db.add(game)
        games_loaded += 1

        if games_loaded % 100 == 0:
            db.commit()
            print(f"Progress: {games_loaded}/{len(df)} games loaded...")

    db.commit()
    print(f"✅ Loaded all {games_loaded} games successfully!")
