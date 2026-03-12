import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.extractor import extract_games_json  # noqa: E402
from src.loader import load_developers, load_games, load_genres  # noqa: E402
from src.transformer import (  # noqa: E402
    transform_games,
    extract_developers,
    extract_genres,
)
from app.database import SessionLocal  # noqa: E402

logger.info("Starting data extraction...")
df = extract_games_json("data/games.json")
logger.info(f"Extracted {len(df)} games")

logger.info("Starting data transformation...")
df_clean = transform_games(df, max_games=15000)
logger.info(f"Transformed to {len(df_clean)} clean games")

logger.info("Extracting developers...")
developers = extract_developers(df_clean)
logger.info(f"Found {len(developers)} developers")

logger.info("Extracting genres...")
genres = extract_genres(df_clean)
logger.info(f"Found {len(genres)} genres")

logger.info("Connecting to database...")
db = SessionLocal()
logger.info("Loading developers...")
dev_map = load_developers(db, developers)
logger.info("Loading genres...")
genre_map = load_genres(db, genres)
logger.info("Loading games...")
load_games(db, df_clean, dev_map, genre_map)
db.close()
logger.info("✅ Data seeding completed successfully!")
print("\n✅ Data seeding completed successfully!")
