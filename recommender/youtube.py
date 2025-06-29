import requests
from decouple import config
from datetime import datetime, timedelta
from recommender.embedder import get_query_embedding, cosine_similarity

YOUTUBE_API_KEY = config("YOUTUBE_API_KEY")


def search_youtube(query, max_results=10, video_duration=None, published_after=None):
    
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    if video_duration:
        params["videoDuration"] = video_duration

    if published_after:
        time_filter = {
            "last_hour": datetime.utcnow() - timedelta(hours=1),
            "today": datetime.utcnow() - timedelta(days=1),
            "this_week": datetime.utcnow() - timedelta(weeks=1),
            "this_month": datetime.utcnow() - timedelta(days=30),
            "this_year": datetime.utcnow() - timedelta(days=365)
        }
        if published_after in time_filter:
            time_value = time_filter[published_after]
            params["publishedAfter"] = time_value.isoformat("T") + "Z"

    response = requests.get(url, params=params)
    data = response.json()
    
    videos = []
    for item in data.get("items", []):
        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })
    return videos

def get_semantic_youtube_recommendations(query, max_results=5, video_duration=None, published_after=None):
    query_embedding = get_query_embedding(query)
    videos = search_youtube(query, max_results=50, video_duration=video_duration, published_after=published_after)

    for video in videos:
        text = f"{video['title']} {video['description']}"
        try:
            video_embedding = get_query_embedding(text)
            video["score"] = float(round(cosine_similarity(query_embedding, video_embedding), 4))
        except Exception:
            video["score"] = 0.0

    return sorted(videos, key=lambda x: x["score"], reverse=True)[:max_results]
