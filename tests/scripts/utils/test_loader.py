from app.database import SessionLocal, engine, Base
from scripts.utils.loader import load_developers, load_genres, load_games
from scripts.utils.transformer import (
    transform_games,
    extract_developers,
    extract_genres,
)
from scripts.utils.extractor import extract_games
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


Base.metadata.create_all(bind=engine)

df = extract_games("data/games.csv", nrows=100)
df_clean = transform_games(df, max_games=50)
developers = extract_developers(df_clean)
genres = extract_genres(df_clean)

db = SessionLocal()
try:
    dev_map = load_developers(db, developers)
    genre_map = load_genres(db, genres)
    load_games(db, df_clean, dev_map, genre_map)
    print("\n✅ Test successful! All data loaded to database.")
except Exception as e:
    print(f"\n❌ Test failed: {e}")
    db.rollback()
finally:
    db.close()
