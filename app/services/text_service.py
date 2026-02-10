import re

from pymongo.collection import Collection


def create_text(collection: Collection, sale_id: int, text: str) -> dict:
    result = collection.insert_one({"sale_id": sale_id, "text": text})
    doc = collection.find_one({"_id": result.inserted_id})
    if doc is None:
        raise ValueError("Failed to insert text document")
    return _serialize_doc(doc)


def search_texts(collection: Collection, query: str) -> list[dict]:
    safe_pattern = re.escape(query)
    docs = collection.find({"text": {"$regex": safe_pattern, "$options": "i"}})
    return [_serialize_doc(doc) for doc in docs]


def delete_texts_by_sale_id(collection: Collection, sale_id: int) -> None:
    collection.delete_many({"sale_id": sale_id})


def _serialize_doc(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc
