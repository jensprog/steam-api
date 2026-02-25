import sys
from pathlib import Path
from src.extractor import extract_games_json
from src.transformer import (
    transform_games,
    extract_developers,
    extract_genres,
)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

df = extract_games_json("data/games.json")

df_clean = transform_games(df, max_games=500)
developers = extract_developers(df_clean)
genres = extract_genres(df_clean)

print("\n✅ Transformation completed successfully!")
print(f"Clean games: {len(df_clean)}")
print(f"Unique developers: {len(developers)}")
print(f"Unique genres: {len(genres)}")
print(f"\nSample transformed data: {list(developers)[:5]}")
print(f"Sample genres: {list(genres)[:5]}")
