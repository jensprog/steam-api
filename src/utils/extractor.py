from pathlib import Path
import pandas as pd
import json


def extract_games_json(json_path: str, max_games: int | None = None) -> pd.DataFrame:
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    print(f"Extracting data from {path}...")
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

        games_list = []
        count = 0
        for app_id, game_data in data.items():
            if max_games and count >= max_games:
                break
            game_data["app_id"] = app_id
            games_list.append(game_data)
            count += 1

    df = pd.DataFrame(games_list)
    if max_games is not None:
        df = df.head(max_games)
    print(f"Extracted {len(df)} rows.")
    return df
