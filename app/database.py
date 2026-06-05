from pymongo import MongoClient
from pymongo.collection import Collection

MONGO_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URL)

db = client["story_db"]
users_collection = db["users"]