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
## 📁 Folder Structure & File Descriptions

genai-recommender/
├── app.py # Streamlit UI (frontend)
├── main.py # FastAPI backend app entry point
├── crud.py # User creation and verification
├── models.py # Pydantic schemas for user input
├── db/
│ └── mongo.py # MongoDB connection & collection setup
├── recommender/
│ ├── youtube.py # YouTube search logic using YouTube API
│ └── embedder.py # Text embedding using Sentence-BERT
├── .env # API keys and environment secrets
├── .gitignore # Files to exclude from Git tracking
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

### 🔍 File Details

| File | Purpose |
|------|---------|
| **`app.py`** | The **frontend** using Streamlit; users interact here. |
| **`main.py`** | The **backend API** built using FastAPI. Handles login, register, recommendations, feedback, etc. |
| **`crud.py`** | Functions for creating/verifying users in MongoDB. |
| **`models.py`** | Pydantic data validation for incoming API requests. |
| **`db/mongo.py`** | MongoDB connection logic and collection access (users, feedback, bookmarks). |
| **`recommender/youtube.py`** | YouTube video search via YouTube API. |
| **`recommender/embedder.py`** | Embedding text using Sentence-BERT and computing cosine similarity. |

---

## 🧪 Setup Instructions

✅  1. Clone the Repository

git clone https://github.com/pallavirani123/genai-recommender.git
cd genai-recommender

✅ 2. Create Virtual Environment (Recommended)

conda create -n genai python=3.9
conda activate genai

✅ 3. Install Required Dependencies

pip install -r requirements.txt

✅ 4. Setup Environment Variables
Create a .env file in the root directory with the following content:

MONGODB_URI=mongodb://localhost:27017/genai_recommender
YOUTUBE_API_KEY=your_actual_youtube_api_key_here
Replace your_actual_youtube_api_key_here with your actual YouTube Data API v3 key.

🚀 How to Run the Project
✅ Step 1: Start the Backend (FastAPI)

uvicorn main:app --reload
Runs at: http://127.0.0.1:8000

API Docs (Swagger UI): http://127.0.0.1:8000/docs

✅ Step 2: Start the Frontend (Streamlit)

streamlit run app.py
Opens in your browser at: http://localhost:8501


📤 Export Bookmarks
Go to the Bookmarks section in the app

Click 📤 Export Bookmarks

A .csv file will download with your saved video list


💡 Example Search Topics
"LLMs for beginners"

"Fine-tuning BERT"

"Computer Vision with Python"

"Data Structures in C++"

---- 

Future Enhancements (Suggestions)

✅ Semantic summary of videos using Whisper + Transformers

🔄 Personalized ranking based on user feedback

📈 Admin dashboard to visualize usage trends

🎯 Personalized daily recommendations via email or Telegram bot

📜 License
This project is licensed under the MIT License.

🙋‍♀️ Author
@pallavirani123 – Passionate about AI, NLP, and building intelligent tools for learning.

🤝 Contributions Welcome
Feel free to fork this repo, create a new branch, and raise a pull request. Let’s build together 🚀
