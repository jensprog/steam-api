# Configures and runs the AsyncIO scheduler that triggers daily game sync from the Steam API.
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import SessionLocal
from app.repositories.sqlalchemy.sync_repository import SQLAlchemySyncRepository
from app.services.steam_sync_service import sync_games

scheduler = AsyncIOScheduler()

def run_sync_job():
    db = SessionLocal()
    try:
        repo = SQLAlchemySyncRepository(db)
        sync_games(repo)
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(run_sync_job, "cron", hour=3, minute=0)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()