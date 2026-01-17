import streamlit as st
import requests
import time
import os
import pickle
import gzip

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ----------------------------
# Custom CSS (Dark Theme + Navbar + Hover)
# ----------------------------
st.markdown("""
<style>
/* Remove Streamlit default padding */
.block-container {
    padding-top: 0rem !important;
}

/* Hide Streamlit footer/menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Background */
.stApp {
    background-color: #0f0f0f;
    color: white;
}

/* Top Navbar */
.navbar {
    background: #000;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #222;
}
.logo {
    font-size: 28px;
    font-weight: 800;
    color: red;
}
.nav-links {
    display: flex;
    gap: 24px;
    font-size: 16px;
}
.nav-links a {
    text-decoration: none;
    color: white;
    opacity: 0.85;
}
.nav-links a:hover {
    opacity: 1;
    color: #ffcc00;
}

/* Menu bar */
.menu-bar {
    background: #111;
    padding: 10px 18px;
    display: flex;
    gap: 18px;
    border-bottom: 1px solid #222;
    font-size: 15px;
}
.menu-item {
    color: white;
    opacity: 0.85;
    cursor: pointer;
}
.menu-item:hover {
    opacity: 1;
    color: #ffcc00;
}

/* Search box right */
.searchbox {
    width: 280px;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #333;
    background: #000;
    color: white;
}

/* Section title */
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin: 18px 0 12px 0;
    border-left: 5px solid #ffcc00;
    padding-left: 12px;
}

/* Poster cards */
.poster-card {
    text-align: center;
    transition: 0.3s;
}
.poster-card img {
    width: 100%;
    border-radius: 14px;
    transition: 0.3s;
}
.poster-card img:hover {
    transform: scale(1.06);
}
.poster-card p {
    margin-top: 8px;
    font-size: 14px;
    color: #ddd;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load files (your model)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(BASE_DIR, "models", "movies.pkl")
similarity_path = os.path.join(BASE_DIR, "models", "similarity.pkl.gz")

movies = pickle.load(open(movies_path, "rb"))
with gzip.open(similarity_path, "rb") as f:
    similarity = pickle.load(f)

movies_list = movies["title"].tolist()

# ----------------------------
# TMDB API Key
# ----------------------------
API_KEY = st.secrets.get("TMDB_API_KEY", None)

@st.cache_data
def fetch_poster(movie_id):
    if not API_KEY:
        return "https://via.placeholder.com/300x450?text=No+API+Key"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    r = requests.get(url)

    if r.status_code != 200:
        return "https://via.placeholder.com/300x450?text=Error"

    data = r.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return "https://via.placeholder.com/300x450?text=No+Image"

# ----------------------------
# Recommendation Function
# ----------------------------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# ----------------------------
# Navbar UI
# ----------------------------
st.markdown("""
<div class="navbar">
    <div class="logo">HDHub4u</div>
    <div class="nav-links">
        <a href="#">Disclaimer</a>
        <a href="#">How To Download?</a>
        <a href="#">Join Our Group!</a>
        <a href="#">Movie Request Page</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Menu bar + Search box
col1, col2 = st.columns([7, 3])
with col1:
    st.markdown("""
    <div class="menu-bar">
        <div class="menu-item">Home 🏠</div>
        <div class="menu-item">Bollywood</div>
        <div class="menu-item">Hollywood</div>
        <div class="menu-item">Hindi Dubbed</div>
        <div class="menu-item">South Hindi</div>
        <div class="menu-item">Web Series</div>
        <div class="menu-item">18+</div>
        <div class="menu-item">Genres</div>
        <div class="menu-item">More</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    search = st.text_input("", placeholder="Search here...")

# ----------------------------
# Featured Posters (Top Strip)
# ----------------------------
st.markdown('<div class="section-title">🔥 Featured</div>', unsafe_allow_html=True)

featured_cols = st.columns(8)
for idx, col in enumerate(featured_cols):
    with col:
        movie_name = movies_list[idx]
        movie_id = movies[movies["title"] == movie_name].iloc[0].id
        poster = fetch_poster(movie_id)

        st.markdown(f"""
        <div class="poster-card">
            <img src="{poster}">
            <p>{movie_name}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Recommender Section
# ----------------------------
st.markdown('<div class="section-title">🎬 Movie Recommender</div>', unsafe_allow_html=True)

option = st.selectbox("Select the movie 📽️", movies_list)

if st.button("Recommend"):
    with st.spinner("Fetching recommendations..."):
        time.sleep(0.2)
        names, posters = recommend(option)

    st.markdown('<div class="section-title">✅ Recommended Movies</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names[:5], posters[:5]):
        with col:
            st.markdown(f"""
            <div class="poster-card">
                <img src="{poster}">
                <p>{name}</p>
            </div>
            """, unsafe_allow_html=True)

    cols2 = st.columns(5)
    for col, name, poster in zip(cols2, names[5:10], posters[5:10]):
        with col:
            st.markdown(f"""
            <div class="poster-card">
                <img src="{poster}">
                <p>{name}</p>
            </div>
            """, unsafe_allow_html=True)
