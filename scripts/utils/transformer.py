import pandas as pd

"""Cleans and transform the extracted games data."""


def transform_games(df: pd.DataFrame, max_games: int = 15000) -> pd.DataFrame:
    print("Transforming data...")

    if "AppID" not in df.columns:
        df = df.reset_index()

    initial_count = len(df)
    df = df.dropna(subset=["Developers", "Genres", "Name"])
    print(f"Dropped {initial_count - len(df)} rows with missing critical data.")

    print(df[["AppID", "Name", "Release date"]].head(1))
    df = df.rename(
        columns={
            "AppID": "app_id",
            "Name": "name",
            "Release date": "release_date",
            "Price": "price",
            "Estimated owners": "estimated_owners",
            "Metacritic score": "metacritic_score",
            "Positive": "positive",
            "Negative": "negative",
            "Average playtime forever": "average_playtime_forever",
            "Header image": "header_image",
            "Windows": "windows",
            "Mac": "mac",
            "Linux": "linux",
            "About the game": "short_description",
        }
    )
    print(df[["app_id", "name", "release_date"]].head(1))
    print(df[["Developers", "Genres"]].head(3))

    if df["price"].max() > 1000:  # Assuming price is in cents if max is very high
        df["price"] = df["price"] / 100.0

    df = df.head(max_games)
    print(f"Transformed data with {len(df)} games ready for loading")
    return df


"""Extract unique developers from the DataFrame."""


def extract_developers(df: pd.DataFrame) -> set:
    developers = set()
    for devs_str in df["Developers"].dropna():
        devs = [d.strip() for d in str(devs_str).split(",")]
        developers.update(devs)

    print(f"Found {len(developers)} unique developers")
    return developers


"""Extract unique genres from the DataFrame."""


def extract_genres(df: pd.DataFrame) -> set:
    genres = set()
    for genres_str in df["Genres"].dropna():
        gens = [g.strip() for g in str(genres_str).split(",")]
        genres.update(gens)

    print(f"Found {len(genres)} unique genres")
    return genres
