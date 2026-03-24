import sys
import os
from pathlib import Path
from app.database import SessionLocal
from sqlalchemy import text

sys.path.append(str(Path(__file__).parent.parent))
os.chdir(str(Path(__file__).parent.parent))


db = SessionLocal()
try:
    db.execute(text("DROP TABLE IF EXISTS game_developers, game_genres, users, games, developers, genres CASCADE"))
    db.commit()
    print("Database cleared")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()
