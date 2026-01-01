
from pymongo import MongoClient
from config import MONGODB_URI
from models import Stats, Hero
from datetime import datetime, timezone



client = MongoClient(MONGODB_URI)
database = client['DunGenDB']
hero_db = database['Heroes']

# Indexes
hero_db.create_index('owner_id')


def create_hero_for_user(user_id: int, name: str, stats: Stats, level: int):
    new_hero = Hero(
        name=name,
        level=level,
        stats=stats,
        HP=stats.MAX_HP,
        owner_id=user_id,
        createdAt=datetime.now(tz=timezone.utc)
    )
    new_hero_doc = new_hero.model_dump(by_alias=True, exclude_none=True)
    hero_db.insert_one(new_hero_doc)
    return new_hero
    

def get_heroes_for_user(user_id: int):
    return hero_db.find({'owner_id': str(user_id)})

def update_hero():
    pass