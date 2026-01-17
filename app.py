import streamlit as st
import pickle
import requests
import time
import os
import gzip

# ----------------------------------------
# Page Config
# ----------------------------------------
st.set_page_config(page_title="Movie Recommender System", layout="wide")

# ----------------------------------------
# Custom CSS (Modern Attractive UI)
# ----------------------------------------
st.markdown("""
<style>
/* App background */
.stApp {
    background: linear-gradient(135deg, #0b1020, #0a0f1a);
    color: white;
}

/* Center title */
h1 {
    text-align: center;
    font-weight: 800;
    font-size: 42px;
    background: -webkit-linear-gradient(#00f5d4, #00bbf9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* Selectbox label */
label {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #ffffff !important;
}

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #00f5d4, #00bbf9);
    color: black;
    font-size: 18px;
    font-weight: 700;
    border: none;
    padding: 10px;
    border-radius: 12px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #00bbf9, #00f5d4);
}

/* Card style */
.movie-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 12px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 8px 22px rgba(0,0,0,0.35);
    transition: 0.3s;
}
.movie-card:hover {
    transform: translateY(-6px);
    border: 1px solid rgba(0,245,212,0.7);
}

/* Poster */
.movie-card img {
    width: 100%;
    border-radius: 14px;
    transition: 0.3s;
}
.movie-card img:hover {
    transform: scale(1.07);
}

/* Movie title */
.movie-title {
    margin-top: 10px;
    font-size: 15px;
    font-weight: 600;
    color: #e8e8e8;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 16px;
    color: rgba(255,255,255,0.75);
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# TMDB API Key (Streamlit Secrets)
# ----------------------------------------
API_KEY = st.secrets.get("TMDB_API_KEY", None)

# ----------------------------------------
# Load model files
# ----------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies_path = os.path.join(BASE_DIR, "models", "movies.pkl")
similarity_path = os.path.join(BASE_DIR, "models", "similarity.pkl.gz")

movies = pickle.load(open(movies_path, "rb"))
with gzip.open(similarity_path, "rb") as f:
    similarity = pickle.load(f)

movies_list = movies["title"].tolist()

# ----------------------------------------
# Title
# ----------------------------------------
st.title("🎬 Movie Recommender System")
st.markdown('<div class="subtitle">Find movies similar to your favourite one ✨</div>', unsafe_allow_html=True)

# ----------------------------------------
# Movie Selection Section
# ----------------------------------------
colA, colB = st.columns([3, 1])

with colA:
    option = st.selectbox("Select the movie 📽️", movies_list)

with colB:
    st.write("")  # spacing
    st.write("")
    recommend_btn = st.button("✨ Recommend")

# ----------------------------------------
# Fetch poster from TMDB
# ----------------------------------------
@st.cache_data
def fetch_poster(movie_id):
    if not API_KEY:
        return "https://via.placeholder.com/300x450?text=No+API+Key"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "https://via.placeholder.com/300x450?text=Error"

    data = response.json()
    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# ----------------------------------------
# Recommendation Function
# ----------------------------------------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# ----------------------------------------
# Recommend Output
# ----------------------------------------
if recommend_btn:
    with st.spinner("Fetching recommendations..."):
        time.sleep(0.3)
        names, posters = recommend(option)

    st.markdown("## ✅ Recommended Movies For You")

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster}" />
                    <div class="movie-title">{name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
