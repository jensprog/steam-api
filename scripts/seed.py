import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from scripts.utils.extractor import extract_games_json  # noqa: E402
from scripts.utils.loader import load_developers, load_games, load_genres  # noqa: E402
from scripts.utils.transformer import (  # noqa: E402
    transform_games,
    extract_developers,
    extract_genres,
)
from app.database import SessionLocal  # noqa: E402

df = extract_games_json("data/games.json")

df_clean = transform_games(df, max_games=15000)
developers = extract_developers(df_clean)
genres = extract_genres(df_clean)

db = SessionLocal()
dev_map = load_developers(db, developers)
genre_map = load_genres(db, genres)
load_games(db, df_clean, dev_map, genre_map)
db.close()

print("\n✅ Data seeding completed successfully!")
