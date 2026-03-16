import sys
import random
import logging
from pathlib import Path
from app.database import SessionLocal, engine, Base
from app.models.game import Game
from app.models.developer import Developer
from app.models.genre import Genre

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent))

logger.info("Creating mock test data...")

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Create mock developers
    developers = [
        Developer(name="Mock Studios"),
        Developer(name="Test Games Inc"),
        Developer(name="Valve"),
        Developer(name="Indie Dev"),
        Developer(name="Big Publisher"),
    ]

    db.add_all(developers)
    db.flush()
    logger.info(f"Created {len(developers)} mock developers")

    # Create mock genres
    genres = [
        Genre(name="Action"),
        Genre(name="RPG"),
        Genre(name="Strategy"),
        Genre(name="Simulation"),
        Genre(name="Adventure"),
    ]

    db.add_all(genres)
    db.flush()
    logger.info(f"Created {len(genres)} mock genres")

    # Create specific games that tests expect
    specific_games = [
        Game(id=1, name="Test Game 1", price=19.99, developer_id=developers[0].id),
        Game(id=100, name="Test Game 100", price=29.99, developer_id=developers[1].id),
        Game(id=500, name="Test Game 500", price=9.99, developer_id=developers[2].id),
        Game(id=5783, name="Counter-Strike", price=0.00, developer_id=developers[2].id),
        Game(id=9790, name="Call of Duty", price=59.99, developer_id=developers[3].id),
        Game(id=11220, name="Portal", price=19.99, developer_id=developers[2].id),
    ]

    # Generate additional random games
    game_names = [
        "Epic Adventure",
        "Space Quest",
        "Dragon Saga",
        "Racing Thunder",
        "Puzzle Master",
        "War Strategy",
        "City Builder",
        "Farm Simulator",
        "Ocean Explorer",
        "Mountain Climber",
        "Time Traveler",
        "Robot Wars",
        "Magic Kingdom",
        "Ninja Strike",
        "Pirate Treasure",
        "Desert Storm",
        "Ice Age",
        "Jungle Run",
        "Sky Fighter",
        "Underground",
    ]

    additional_games = []
    used_ids = {1, 100, 500, 5783, 9790, 11220}

    for i in range(94):  # 94 + 6 specific = 100 total
        game_id = i + 2000  # Start from 2000 to avoid conflicts
        while game_id in used_ids:
            game_id += 1
        used_ids.add(game_id)

        game = Game(
            id=game_id,
            name=f"{random.choice(game_names)} {game_id}",
            price=round(random.uniform(5.99, 69.99), 2),
            developer_id=random.choice(developers).id,
        )
        additional_games.append(game)

    all_games = specific_games + additional_games
    db.add_all(all_games)

    # Add genres to games (many-to-many relationship)
    for game in all_games:
        # Add 1-3 random genres to each game
        num_genres = random.randint(1, 3)
        game_genres = random.sample(genres, num_genres)
        game.genres.extend(game_genres)

    db.commit()
    logger.info(f"Created {len(all_games)} mock games with genres")
    logger.info("Mock data seeding completed successfully!")

except Exception as e:
    db.rollback()
    logger.error(f"Error creating mock data: {e}")
    raise
finally:
    db.close()

print("\nMock data seeding completed successfully!")
