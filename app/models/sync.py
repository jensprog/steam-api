# Tracks the last sync timestamp used to determine what data to fetch from Steam API.
from sqlalchemy import Column, Integer, DateTime, Boolean
from app.database import Base


class SyncState(Base):
    __tablename__ = "sync_state"
    id = Column(Integer, primary_key=True)
    last_sync_timestamp = Column(DateTime)
    catch_up_completed = Column(Boolean, default=False)
