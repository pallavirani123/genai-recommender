from database import user_collection
from models import UserCreate

async def create_user(user: UserCreate):
    user_dict = user.dict()
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        return {"message": "User already exists"}
    await user_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}

async def verify_user(email: str, password: str):
    user = await user_collection.find_one({"email": email, "password": password})
    return user
