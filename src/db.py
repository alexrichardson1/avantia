import requests
import os
from pymongo import MongoClient


def get_collection():
    client = MongoClient(os.environ["MONGO_URI"])
    db = client["nobel_prizes"]
    collection = db["laureates"]
    return collection


def seed():
    response = requests.get(os.environ["DATASET_URL"])
    data = response.json()
    collection = get_collection()

    for prize in data["prizes"]:
        for laureate in prize.get("laureates", []):
            laureate_data = {
                "firstname": laureate.get("firstname", ""),
                "surname": laureate.get("surname", ""),
                "motivation": laureate.get("motivation", ""),
                "category": prize.get("category", ""),
            }
            collection.insert_one(laureate_data)
