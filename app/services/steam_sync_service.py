# Fetches app list and game details from the Steam API and syncs them to the database.
from typing import List
import requests
from app.core.config import settings
from app.repositories.interfaces.sync_repository import SyncRepositoryInterface
from app.schemas.sync import SteamAppData
from datetime import datetime


def get_app_list_from_steam_api(sync_repo: SyncRepositoryInterface) -> List[dict]:
    timestamp = sync_repo.get_last_sync_timestamp()
    params = {"key": settings.STEAM_API_KEY}

    if timestamp:
        params["if_modified_since"] = int(timestamp.timestamp())

    response = requests.get("https://api.steampowered.com/IStoreService/GetAppList/v1/", params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("response", {}).get("apps", [])


def get_app_details(app_id):
    response = requests.get("https://store.steampowered.com/api/appdetails", params={"appids": app_id})
    data = response.json()

    if data is None:
        return None

    return data.get(str(app_id), {}).get("data")


def sync_games(sync_repo: SyncRepositoryInterface) -> None:
    data = get_app_list_from_steam_api(sync_repo)

    for game in data:
        app_id = game["appid"]
        result = get_app_details(app_id)

        if result is None:
            continue

        result["app_id"] = str(app_id)
        game_data = SteamAppData.model_validate(result)
        sync_repo.upsert_game(game_data)

    sync_repo.update_last_sync_timestamp(datetime.now())
