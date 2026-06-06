import sys
from app.services.steam_sync_service import get_app_details
from app.repositories.sqlalchemy.sync_repository import SQLAlchemySyncRepository
from app.schemas.sync import SteamAppData
from app.database import SessionLocal


def resync_game(app_id: int) -> None:
    result = get_app_details(app_id)
    if result is None:
        print(f"No data returned from Steam for app_id {app_id}")
        return

    result["app_id"] = str(app_id)
    game_data = SteamAppData.model_validate(result)

    db = SessionLocal()
    try:
        repo = SQLAlchemySyncRepository(db)
        repo.upsert_game(game_data)
        print(f"Successfully re-synced app_id {app_id} ({game_data.name})")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/resync_game.py <app_id>")
        sys.exit(1)

    resync_game(int(sys.argv[1]))
