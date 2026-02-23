import sys
from pathlib import Path
from scripts.utils.extractor import extract_games

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


df = extract_games("data/games.csv", nrows=100)


print(f"\n✅ Successfully extracted {len(df)} rows")
print(f"\nColumns: {df.columns.tolist()}")
print("\nFirst 3 rows:")
print(df.head(3))
print("\nData types:")
print(df.dtypes)
