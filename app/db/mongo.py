from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from app.core.config import get_settings

settings = get_settings()
client = MongoClient(settings.mongo_uri)


def get_text_collection() -> Collection:
    db = client[settings.mongo_db_name]
    return db[settings.mongo_collection_name]


def create_indexes() -> None:
    try:
        collection = get_text_collection()
        collection.create_index([("sale_id", ASCENDING)])
        collection.create_index([("text", ASCENDING)])
    except PyMongoError:
        # Mongo can be started after the API; indexes will be created on first successful startup.
        pass
