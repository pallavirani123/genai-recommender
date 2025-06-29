from fastapi import FastAPI, HTTPException, Query, Depends, Body
from typing import Optional
from models import UserCreate,UserLogin
from crud import create_user,verify_user
from recommender.embedder import get_query_embedding, cosine_similarity
from recommender.youtube import search_youtube, get_semantic_youtube_recommendations
from db.mongo import feedback_collection
from pymongo.collection import Collection
from datetime import datetime
from bson import ObjectId
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
from transformers import pipeline
from db.mongo import bookmarks_collection

app = FastAPI()

@app.post("/login_user")
async def login_user(user: UserLogin):
    existing_user = await verify_user(user.email, user.password)
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "email": user.email}

@app.get("/")
def read_root():
    return {"message": "GenAI Learning Recommender API is up."}
    

@app.post("/register_user")
async def register_user(user: UserCreate):
    result = await create_user(user)
    if "already exists" in result["message"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/embed_query")
async def embed_query(query: str):
    embedding = get_query_embedding(query)
    return {"embedding": embedding.tolist()}

@app.get("/recommend/youtube")
def recommend_youtube(
    query: str,
    max_results: int = 5,
    video_duration: Optional[str] = Query(None),
    published_after: Optional[str] = Query(None)
):
    return get_semantic_youtube_recommendations(
        query=query,
        max_results=max_results,
        video_duration=video_duration,
        published_after=published_after
    )

    
@app.post("/feedback")
def store_feedback(user_id: str, video_id: str, title: str, url: str, feedback: str):
    if feedback not in ["like", "dislike"]:
        raise HTTPException(status_code=400, detail="Feedback must be 'like' or 'dislike'")

    feedback_data = {
        "user_id": user_id,
        "video_id": video_id,
        "title": title,
        "url": url,
        "feedback": feedback,
        "timestamp": datetime.utcnow()
    }

    feedback_collection.insert_one(feedback_data)
    return {"message": "Feedback stored successfully"}

@app.get("/feedback/likes")
def get_liked_videos(user_id: str):
    likes = list(feedback_collection.find({"user_id": user_id, "feedback": "like"}))
    for like in likes:
        like["_id"] = str(like["_id"])  # Convert ObjectId to string
    return likes

@app.delete("/feedback/remove_like")
def remove_liked_video(user_id: str = Query(...), video_id: str = Query(...)):
    result = feedback_collection.delete_one({
        "user_id": user_id,
        "video_id": video_id,
        "feedback": "like"
    })
    if result.deleted_count:
        return {"message": "Like removed"}
    raise HTTPException(status_code=404, detail="Liked video not found")

@app.post("/bookmarks/add")
def add_bookmark(user_id: str, video_id: str, title: str, url: str, score: float = 0.0):
    if bookmarks_collection.find_one({"user_id": user_id, "video_id": video_id}):
        return {"message": "Already bookmarked."}

    bookmark = {
        "user_id": user_id,
        "video_id": video_id,
        "title": title,
        "url": url,
        "score": score,
        "timestamp": datetime.utcnow()
    }
    bookmarks_collection.insert_one(bookmark)
    return {"message": "Bookmark added."}

@app.get("/bookmarks/get")
def get_bookmarks(user_id: str):
    print(f"Fetching bookmarks for: {user_id}")
    bookmarks = list(bookmarks_collection.find({"user_id": user_id}))
    for bm in bookmarks:
        bm["_id"] = str(bm["_id"])
    return bookmarks


@app.delete("/bookmarks/remove")
def remove_bookmark(user_id: str = Query(...), video_id: str = Query(...)):
    result = bookmarks_collection.delete_one({"user_id": user_id, "video_id": video_id})
    if result.deleted_count:
        return {"message": "Bookmark removed."}
    raise HTTPException(status_code=404, detail="Bookmark not found")

