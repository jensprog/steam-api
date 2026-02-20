import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from scripts.utils.extractor import extract_games
from scripts.utils.transformer import (
    transform_games,
    extract_developers,
    extract_genres,
)

df = extract_games("data/games.csv", nrows=1000)

df_clean = transform_games(df, max_games=500)
developers = extract_developers(df_clean)
genres = extract_genres(df_clean)

print(f"\n✅ Transformation completed successfully!")
print(f"Clean games: {len(df_clean)}")
print(f"Unique developers: {len(developers)}")
print(f"Unique genres: {len(genres)}")
print(f"\nSample transformed data: {list(developers)[:5]}")
print(f"Sample genres: {list(genres)[:5]}")
