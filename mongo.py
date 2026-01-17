from datetime import datetime, timezone
from typing import Any, List

from pydantic_core import ValidationError
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from config import MONGODB_URI
from models import Hero, Stats

# MongoDB Setup
client: MongoClient[Any] = MongoClient(MONGODB_URI)
database: Database[Any] = client["DunGenDB"]
hero_db: Collection[Any] = database["Heroes"]

# Indexes
hero_db.create_index("owner_id")


def create_hero_for_user(user_id: int, name: str, stats: Stats, level: int) -> Hero:
    """Creates a new Hero Document in the database with provided user as owner"""
    new_hero = Hero(
        name=name,
        level=level,
        stats=stats,
        HP=stats.MAX_HP,
        owner_id=str(user_id),
        created_at=datetime.now(tz=timezone.utc),
    )
    new_hero_doc = new_hero.model_dump(by_alias=True, exclude_none=True)
    hero_db.insert_one(new_hero_doc)
    return new_hero


def get_heroes_for_user(user_id: int) -> List[Hero]:
    """Fetches all Heroes owned by a specific user from the database"""
    hero_docs = hero_db.find({"owner_id": str(user_id)})
    heroes: List[Hero] = []
    for doc in hero_docs:
        try:
            h = Hero.model_validate(doc)
            heroes.append(h)
        except ValidationError as e:
            print(f"Error validating Hero document {doc.get('_id')}: {e}")
            continue
    return heroes


def update_hero(hero_id: str, updates: dict[str, Any]) -> None:
    """Updates specified fields of a Hero in the database"""
    hero_db.update_one({"_id": hero_id}, {"$set": updates})
