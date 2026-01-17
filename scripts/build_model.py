import pandas as pd
import ast
import pickle
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Load dataset (MATCHES YOUR FILE NAME)
# --------------------------------------------------
df = pd.read_csv("data/movie_dataset.csv")


# --------------------------------------------------
# 2. Select required columns
# --------------------------------------------------
df = df[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]


# --------------------------------------------------
# 3. Helper functions (SAFE parsing)
# --------------------------------------------------
def convert(text):
    try:
        return " ".join([i['name'] for i in ast.literal_eval(text)])
    except:
        return ""

def convert_cast(text):
    try:
        return " ".join([i['name'] for i in ast.literal_eval(text)[:3]])
    except:
        return ""

def get_director(text):
    try:
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                return i['name']
    except:
        return ""
    return ""


# --------------------------------------------------
# 4. Apply feature extraction
# --------------------------------------------------
df['genres'] = df['genres'].apply(convert)
df['keywords'] = df['keywords'].apply(convert)
df['cast'] = df['cast'].apply(convert_cast)
df['director'] = df['crew'].apply(get_director)


# --------------------------------------------------
# 5. CLEAN ALL TEXT (CRITICAL FIX)
# --------------------------------------------------
df['overview'] = df['overview'].fillna('')
df['genres'] = df['genres'].fillna('')
df['keywords'] = df['keywords'].fillna('')
df['cast'] = df['cast'].fillna('')
df['director'] = df['director'].fillna('')


# --------------------------------------------------
# 6. Create tags (CONTENT FEATURE)
# --------------------------------------------------
df['tags'] = (
    df['overview'].astype(str) + " " +
    df['genres'].astype(str) + " " +
    df['keywords'].astype(str) + " " +
    df['cast'].astype(str) + " " +
    df['director'].astype(str)
).str.lower()

# Remove empty / bad rows
df = df[df['tags'].notna()]
df = df[df['tags'].str.strip() != ""]


# --------------------------------------------------
# 7. Vectorization
# --------------------------------------------------
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()


# --------------------------------------------------
# 8. Cosine similarity (THE MODEL)
# --------------------------------------------------
similarity = cosine_similarity(vectors)


# --------------------------------------------------
# 9. Save model files
# --------------------------------------------------
os.makedirs("models", exist_ok=True)

pickle.dump(df[['id', 'title']], open("models/movies.pkl", "wb"))
pickle.dump(similarity, open("models/similarity.pkl", "wb"))


# --------------------------------------------------
# 10. Done
# --------------------------------------------------
print("✅ Model built successfully")
print(f"📦 Movies saved: {df.shape[0]}")
print(f"📐 Similarity matrix shape: {similarity.shape}")
