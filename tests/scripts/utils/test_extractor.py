import sys
from pathlib import Path
from src.extractor import extract_games_json

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


df = extract_games_json("data/games.json")


print(f"\n✅ Successfully extracted {len(df)} rows")
print(f"\nColumns: {df.columns.tolist()}")
print("\nFirst 3 rows:")
print(df.head(3))
print("\nData types:")
print(df.dtypes)
