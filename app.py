import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

# --- Page Config ---
st.set_page_config(page_title="GenAI YouTube Recommender", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .title {
            font-size: 2em; font-weight: bold; margin-bottom: 10px; color: #66d9ef;
        }
        .card {
            border: 1px solid #333;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #1e222a;
        }
        .stButton>button {
            background-color: #333 !important;
            color: #fff;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #007bff !important;
        }
        .stDownloadButton > button {
            width: 100%;
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Session State Init ---
for key in ["logged_in", "user_email", "history", "last_videos", "view"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else "" if key == "user_email" else []

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<div class='title'>🔐 Welcome to GenAI Recommender</div>", unsafe_allow_html=True)
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🔓 Login"):
            try:
                res = requests.post(f"{BACKEND_URL}/login_user", json={"email": email, "password": password})
                if res.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials.")
            except Exception as e:
                st.error(f"Error: {e}")

    with col2:
        if st.button("📝 Register"):
            try:
                name = email.split("@")[0]
                res = requests.post(f"{BACKEND_URL}/register_user", json={
                    "name": name,
                    "email": email,
                    "password": password,
                    "level": "beginner",
                    "preferred_topics": [],
                    "learning_style": "visual"
                })
                if res.status_code == 200:
                    st.success("✅ Registered! Please log in.")
                else:
                    st.error(res.json().get("detail", "Registration failed."))
            except Exception as e:
                st.error(f"Error: {e}")

# --- MAIN APP ---
else:
    st.markdown("<div class='title'>🎥 GenAI YouTube Recommender</div>", unsafe_allow_html=True)

    # --- Logout ---
    if st.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # --- Filters ---
    col_query, col_duration, col_upload, col_count = st.columns([4, 2, 2, 2])
    query = col_query.text_input("🔍 Search Topic", placeholder="Search YouTube educational content using GenAI magic!")
    duration = col_duration.selectbox("⏱ Duration", ["any", "short (<4 min)", "medium (4-20 min)", "long (>20 min)"])
    upload = col_upload.selectbox("📅 Upload Date", ["any", "last hour", "today", "this week", "this month", "this year"])
    max_results = col_count.selectbox("🎞️ Number of Videos", [3, 5, 10, 15, 20], index=1)

    # --- Top Buttons ---
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("🔍 Search"):
        st.session_state.view = "search"
        try:
            duration_map = {"any": None, "short (<4 min)": "short", "medium (4-20 min)": "medium", "long (>20 min)": "long"}
            upload_map = {"any": None, "last hour": "last_hour", "today": "today", "this week": "this_week", "this month": "this_month", "this year": "this_year"}
            params = {"query": query, "max_results": max_results}
            if duration_map[duration]:
                params["video_duration"] = duration_map[duration]
            if upload_map[upload]:
                params["published_after"] = upload_map[upload]
            res = requests.get(f"{BACKEND_URL}/recommend/youtube", params=params)
            st.session_state.last_videos = res.json()
        except Exception as e:
            st.error(f"Search failed: {e}")
            st.session_state.last_videos = []

    if col2.button("❤️ Likes"):
        st.session_state.view = "liked"
    if col3.button("🔖 Bookmarks"):
        st.session_state.view = "bookmarks"
    if col4.button("📜 History"):
        st.session_state.view = "history"
    if col5.button("📤 Export Bookmarks"):
        try:
            bookmarks = requests.get(f"{BACKEND_URL}/bookmarks/get", params={"user_id": st.session_state.user_email}).json()
            df = pd.DataFrame(bookmarks)
            st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="bookmarks.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Export failed: {e}")

    st.markdown("---")

    # ---------------- VIEW SECTION ----------------
    view = st.session_state.view
    if view == "search":
        if not st.session_state.last_videos:
            st.info("🔍 Use the search bar above to find recommended YouTube videos.")
        else:
            for i, video in enumerate(st.session_state.last_videos):
                with st.container():
                    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                    st.subheader(video["title"])
                    st.markdown(f"**Score:** `{video.get('score', 0):.2f}`")
                    st.image(f"https://img.youtube.com/vi/{video['video_id']}/0.jpg", width=320)
                    st.markdown(f"[▶️ Watch](https://www.youtube.com/watch?v={video['video_id']})")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("👍 Like", key=f"like_{i}"):
                            requests.post(f"{BACKEND_URL}/feedback", params={
                                "user_id": st.session_state.user_email,
                                "video_id": video["video_id"],
                                "title": video["title"],
                                "url": video["url"],
                                "feedback": "like"
                            })
                            st.success("Liked!")

                    with col2:
                        if st.button("👎 Dislike", key=f"dislike_{i}"):
                            requests.post(f"{BACKEND_URL}/feedback", params={
                                "user_id": st.session_state.user_email,
                                "video_id": video["video_id"],
                                "title": video["title"],
                                "url": video["url"],
                                "feedback": "dislike"
                            })
                            st.warning("Disliked!")

                    with col3:
                        if st.button("🔖 Bookmark", key=f"bookmark_{i}"):
                            requests.post(f"{BACKEND_URL}/bookmarks/add", params={
                                "user_id": st.session_state.user_email,
                                "video_id": video["video_id"],
                                "title": video["title"],
                                "url": video["url"],
                                "score": video.get("score", 0)
                            })
                            st.success("Bookmarked!")

                    st.markdown("</div>", unsafe_allow_html=True)

                    if not any(v["url"] == video["url"] for v in st.session_state.history):
                        st.session_state.history.append({
                            "title": video["title"],
                            "url": video["url"],
                            "score": video.get("score", 0)
                        })

    elif view == "liked":
        st.subheader("❤️ Your Liked Videos")
        try:
            liked = requests.get(f"{BACKEND_URL}/feedback/likes", params={"user_id": st.session_state.user_email}).json()
            for video in liked:
                st.markdown(f"- [{video['title']}]({video['url']})")
        except Exception as e:
            st.error(f"Failed to fetch likes: {e}")

    elif view == "bookmarks":
        st.subheader("🔖 Your Bookmarks")
        try:
            bookmarks = requests.get(f"{BACKEND_URL}/bookmarks/get", params={"user_id": st.session_state.user_email}).json()
            for bm in bookmarks:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"🔗 [{bm['title']}]({bm['url']}) — Score: `{bm.get('score', 0):.2f}`")
                with col2:
                    if st.button("🗑️ Remove", key=f"remove_bm_{bm['video_id']}"):
                        requests.delete(f"{BACKEND_URL}/bookmarks/remove", params={
                            "user_id": st.session_state.user_email,
                            "video_id": bm["video_id"]
                        })
                        st.rerun()
        except Exception as e:
            st.error(f"Failed to fetch bookmarks: {e}")

    elif view == "history":
        st.subheader("📜 Viewing History")
        for idx, item in enumerate(st.session_state.history[-10:], 1):
            st.markdown(f"**{idx}. [{item['title']}]({item['url']})** — Score: `{item['score']:.2f}`")
