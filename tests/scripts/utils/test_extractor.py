import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from scripts.utils.extractor import extract_games

df = extract_games("data/games.csv", nrows=100)


print(f"\n✅ Successfully extracted {len(df)} rows")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst 3 rows:")
print(df.head(3))
print(f"\nData types:")
print(df.dtypes)
