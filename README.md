
🎬 Movie Recommender System

A content-based movie recommendation system built using the TMDB movie dataset.
The system recommends movies similar to a selected movie based on plot, genres, keywords, cast, and director, and displays posters using the TMDB API through an interactive Streamlit web app.


🚀 Features

🎥 Content-based movie recommendations

🧠 Cosine similarity on movie metadata

🎭 Uses genres, overview, keywords, cast, and director

🖼️ Movie posters fetched via TMDB API

⚡ Fast and interactive Streamlit UI

🔐 Secure API key handling using .env

📦 Clean and modular project structure


🛠️ Tech Stack

Programming Language: Python

Web Framework: Streamlit

Machine Learning: Scikit-learn

Data Handling: Pandas, NumPy

Vectorization: CountVectorizer

Similarity Measure: Cosine Similarity

API: TMDB (The Movie Database)


📂 Project Structure
Movie_Recommender_System/
│
├── app.py                      # Streamlit application
│
├── data/
│   └── movie_dataset.csv       # TMDB dataset
│
├── models/
│   ├── movies.pkl              # Processed movie metadata
│   └── similarity.pkl          # Cosine similarity matrix
│
├── scripts/
│   └── build_model.py          # Model building script
│
├── notebooks/
│   └── model_building.ipynb    # EDA & experimentation
│
├── requirements.txt            # Dependencies
├── .env                        # TMDB API key (not committed)
├── .gitignore
└── README.md


🧠 How the Recommendation Works

Movie metadata is combined into a single tags feature:

Overview

Genres

Keywords

Top cast

Director

Text is converted into numerical vectors using CountVectorizer

Cosine similarity is computed between all movies

When a user selects a movie, the system:

Finds the most similar movies

Displays top 5 recommendations with posters


⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/Movie_Recommender_System.git
cd Movie_Recommender_System

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Get TMDB API Key

Visit 👉 https://www.themoviedb.org/

Create an account

Go to Profile → Settings → API

Generate an API key

4️⃣ Create .env File

Create a file named .env in the project root:

TMDB_API_KEY=your_tmdb_api_key_here


⚠️ Do not share or commit this file

5️⃣ Build the Recommendation Model
python scripts/build_model.py


This generates:

models/movies.pkl

models/similarity.pkl

6️⃣ Run the Application
python -m streamlit run app.py


Open in browser:

http://localhost:8501


🎯 Usage

Select a movie from the dropdown

Click Recommend

View top 5 similar movies with posters

📊 Dataset

Source: TMDB (The Movie Database)

Movies: ~5000

Features Used:
overview, genres, keywords, cast, crew, title, id


🔒 Security Best Practices

API keys are stored in .env

.env is excluded via .gitignore

No sensitive data is hardcoded

📈 Future Enhancements

🔍 Search with autocomplete

🎭 Genre and language filters

⭐ Rating-based ranking

🤝 Hybrid recommender (content + popularity)

🌍 Deployment on Streamlit Cloud

⚛️ React frontend + FastAPI backend


🧪 Model Type

Approach: Content-Based Filtering

Learning Type: Unsupervised

Similarity Metric: Cosine Similarity


🧑‍💻 Author

Mohit
📌 Movie Recommender System Project
🎓 Machine Learning / Data Science

📝 License

This project is for educational purposes only.
TMDB data and images are used according to TMDB API terms.
