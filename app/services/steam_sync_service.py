# Fetches app list and game details from the Steam API and syncs them to the database.
from typing import List
import requests
import time
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
        time.sleep(1.5)
        result = get_app_details(app_id)

        if result is None:
            continue

        result["app_id"] = str(app_id)
        try:
            game_data = SteamAppData.model_validate(result)
            sync_repo.upsert_game(game_data)
        except Exception:
            continue

    sync_repo.update_last_sync_timestamp(datetime.now())


def catch_up_sync(from_date: datetime, sync_repo: SyncRepositoryInterface) -> None:
    params = {
        "key": settings.STEAM_API_KEY,
        "if_modified_since": int(from_date.timestamp()),
    }
    response = requests.get("https://api.steampowered.com/IStoreService/GetAppList/v1/", params=params)
    response.raise_for_status()
    apps = response.json().get("response", {}).get("apps", [])

    for game in apps:
        app_id = game["appid"]
        time.sleep(1.5)
        result = get_app_details(app_id)

        if result is None:
            continue

        result["app_id"] = str(app_id)
        try:
            game_data = SteamAppData.model_validate(result)
            sync_repo.upsert_game(game_data)
        except Exception:
            continue

    sync_repo.mark_catch_up_completed()
