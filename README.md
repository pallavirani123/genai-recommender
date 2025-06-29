# 🎥 GenAI YouTube Recommender

An intelligent YouTube video recommender system that leverages **semantic search** using Sentence-BERT to suggest educational content tailored to your interests, learning style, and preferences.

## 🔍 Features

- 🔐 **User Authentication** (Login/Register)
- 🔎 **Smart Search**: Search for any topic and get semantically ranked YouTube videos.
- ⏱ **Filters**: Filter by video duration and upload date.
- ❤️ **Like / Dislike** feedback for better personalization.
- 🔖 **Bookmark** videos for future reference (stored in MongoDB).
- 📜 **History Tracking** (per session).
- 📤 **Export Bookmarks** to CSV.
- 🌙 **Dark Mode UI** using custom Streamlit styling.

---

## 🧠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Database**: MongoDB
- **APIs**: YouTube Data API v3, Hugging Face Transformers

---

## 🚀 How It Works

1. **Enter a topic** in the search bar (e.g., *"generative AI for beginners"*).
2. The backend fetches YouTube videos using the YouTube API.
3. Each video is semantically compared with your query using BERT embeddings.
4. Results are ranked by cosine similarity and displayed with filters.

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/pallavirani123/genai-recommender.git
cd genai-recommender
