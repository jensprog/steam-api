# Fetches app list and game details from the Steam API and syncs them to the database.
import logging
import requests
import time
from app.core.config import settings
from app.repositories.interfaces.sync_repository import SyncRepositoryInterface
from app.schemas.sync import SteamAppData
from datetime import datetime

logger = logging.getLogger(__name__)


def get_app_list_from_steam_api(sync_repo: SyncRepositoryInterface) -> list[dict]:
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
        except Exception as e:
            logger.error("sync_games failed for app_id %s: %s", app_id, e)
            continue

    sync_repo.update_last_sync_timestamp(datetime.now())


def gap_sync(sync_repo: SyncRepositoryInterface) -> None:
    response = requests.get(
        "https://api.steampowered.com/IStoreService/GetAppList/v1/",
        params={"key": settings.STEAM_API_KEY},
    )
    response.raise_for_status()
    all_steam_ids = {app["appid"] for app in response.json().get("response", {}).get("apps", [])}

    existing_ids = sync_repo.get_all_app_ids()
    missing_ids = sorted(all_steam_ids - existing_ids)

    checkpoint = sync_repo.get_gap_sync_checkpoint()
    if checkpoint is not None:
        missing_ids = [app_id for app_id in missing_ids if app_id > checkpoint]

    for app_id in missing_ids:
        time.sleep(1.5)
        result = get_app_details(app_id)
        if result is None:
            sync_repo.set_gap_sync_checkpoint(app_id)
            continue
        result["app_id"] = str(app_id)
        try:
            game_data = SteamAppData.model_validate(result)
            sync_repo.upsert_game(game_data)
        except Exception as e:
            logger.error("gap_sync failed for app_id %s: %s", app_id, e)
        sync_repo.set_gap_sync_checkpoint(app_id)

    sync_repo.set_gap_sync_checkpoint(None)
