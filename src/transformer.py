import pandas as pd

"""Cleans and transform the extracted games data."""


def transform_games(df: pd.DataFrame, max_games: int = None) -> pd.DataFrame:
    print("Transforming data...")

    initial_count = len(df)
    df = df.dropna(subset=["developers", "genres", "name"])
    print(f"Dropped {initial_count - len(df)} rows with missing critical data.")

    if df["price"].max() > 1000:  # Assuming price is in cents if max is very high
        df["price"] = df["price"] / 100.0

    if max_games is not None:
        df = df.head(max_games)
    print(f"Transformed data with {len(df)} games ready for loading")
    return df


"""Extract unique developers from the DataFrame."""


def extract_developers(df: pd.DataFrame) -> set:
    developers = set()
    for devs_list in df["developers"].dropna():
        if isinstance(devs_list, list):
            for dev in devs_list:
                developers.add(dev.strip())
        elif isinstance(devs_list, str):
            devs = [d.strip() for d in devs_list.split(",")]
            developers.update(devs)

    print(f"Found {len(developers)} unique developers")
    return developers


"""Extract unique genres from the DataFrame."""


def extract_genres(df: pd.DataFrame) -> set:
    genres = set()
    for genres_list in df["genres"].dropna():
        if isinstance(genres_list, list):
            for genre in genres_list:
                genres.add(genre.strip())
        elif isinstance(genres_list, str):
            gens = [g.strip() for g in genres_list.split(",")]
            genres.update(gens)

    print(f"Found {len(genres)} unique genres")
    return genres
