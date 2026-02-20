from pathlib import Path
import pandas as pd


def extract_games(csv_path: str, nrows: int | None = None) -> pd.DataFrame:
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    print(f"Extracting data from {path}...")
    df = pd.read_csv(path, nrows=nrows)
    print(f"Extracted {len(df)} rows.")
    return df
