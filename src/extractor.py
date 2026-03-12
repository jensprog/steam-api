from pathlib import Path
import pandas as pd
import ijson


def extract_games_json(json_path: str, max_games: int | None = None) -> pd.DataFrame:
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    print(f"Extracting data from {path}...")

    games_list = []
    count = 0

    with open(path, "rb") as file:
        parser = ijson.kvitems(file, "", use_float=True)

        for app_id, game_data in parser:
            if max_games and count >= max_games:
                break

            if isinstance(game_data, dict):
                game_data["app_id"] = app_id
                games_list.append(game_data)
                count += 1

    df = pd.DataFrame(games_list)
    print(f"Extracted {len(df)} rows.")
    return df
