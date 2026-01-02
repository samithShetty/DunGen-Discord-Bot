from datetime import datetime, timezone
from typing import List

from pymongo import MongoClient

from config import MONGODB_URI
from models import Hero, Stats

client = MongoClient(MONGODB_URI)
database = client["DunGenDB"]
hero_db = database["Heroes"]

# Indexes
hero_db.create_index("owner_id")


def create_hero_for_user(user_id: int, name: str, stats: Stats, level: int) -> Hero:
    new_hero = Hero(
        name=name,
        level=level,
        stats=stats,
        HP=stats.MAX_HP,
        owner_id=user_id,
        createdAt=datetime.now(tz=timezone.utc),
    )
    new_hero_doc = new_hero.model_dump(by_alias=True, exclude_none=True)
    hero_db.insert_one(new_hero_doc)
    return new_hero


def get_heroes_for_user(user_id: int) -> List[Hero]:
    cursor = hero_db.find({"owner_id": str(user_id)})
    return [Hero.model_validate(doc) for doc in cursor]


def update_hero():
    pass
