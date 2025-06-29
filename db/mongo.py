from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGODB_URI", default="mongodb://localhost:27017/genai_recommender"))

db = client["genai_recommender"]
feedback_collection = db["feedback"]
bookmarks_collection = db["bookmarks"]
user_collection = db.get_collection("users") 

