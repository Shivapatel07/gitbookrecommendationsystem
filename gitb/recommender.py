# recommender.py
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# Load dataset
df = pd.read_csv("Filtered_Popular_Books.csv")

# Clean text
def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
    return text

df['Title'] = df['Title'].apply(clean_text)
df['Author'] = df['Author'].apply(clean_text)
df['Published'] = df['Published'].astype(str).str.strip()

# Combine text features for TF-IDF
df['Features'] = df['Title'] + " " + df['Author']
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Content-based filtering
def content_based_recommend(book_name, n_recommendations=10):
    if book_name not in df['Title'].values:
        return []
    book_idx = df[df['Title'] == book_name].index[0]
    sim_scores = list(enumerate(cosine_sim[book_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n_recommendations+1]
    return [(df.iloc[i[0]]['Title'], i[1]) for i in sim_scores]

# Collaborative filtering
# Create interaction matrix
interaction_matrix = df.pivot_table(index='Title', values='Shelvings', aggfunc='sum')
scaler = MinMaxScaler()
interaction_matrix_scaled = scaler.fit_transform(interaction_matrix)
interaction_matrix = pd.DataFrame(interaction_matrix_scaled, index=interaction_matrix.index, columns=['Shelvings_Scaled'])

# Train KNN model
knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
knn_model.fit(interaction_matrix.to_numpy())

def collaborative_recommend(book_name, n_recommendations=10):
    if book_name not in interaction_matrix.index:
        return []
    book_idx = np.where(interaction_matrix.index == book_name)[0][0]
    distances, indices = knn_model.kneighbors(interaction_matrix.iloc[book_idx].values.reshape(1, -1), n_neighbors=n_recommendations+1)
    return [(interaction_matrix.index[i], 1 - distances[0][j]) for j, i in enumerate(indices[0]) if j != 0]

# Hybrid recommender
def hybrid_recommend(book_name, content_weight=0.7, collab_weight=0.3, n_recommendations=10):
    content_recs = content_based_recommend(book_name, n_recommendations)
    content_recs = {title: score for title, score in content_recs}
    collab_recs = collaborative_recommend(book_name, n_recommendations)
    collab_recs = {title: score for title, score in collab_recs}

    combined_recs = {}
    for title in set(content_recs.keys()).union(collab_recs.keys()):
        combined_recs[title] = content_recs.get(title, 0) * content_weight + collab_recs.get(title, 0) * collab_weight

    sorted_recommendations = sorted(combined_recs.items(), key=lambda x: x[1], reverse=True)
    return sorted_recommendations[:n_recommendations]

# Function to generate Amazon link
def get_amazon_link(book_title):
    return f"https://www.amazon.in/s?k={book_title.replace(' ', '+')}"

# Popular books based on ratings and shelvings
def popular_books(n=10, min_shelvings=50000, min_ratings=4.0):
    filtered = df[(df["Shelvings"] >= min_shelvings) & (df["Ratings"] >= min_ratings)]
    return filtered.sort_values(by="Shelvings", ascending=False).head(n)[["Title", "Shelvings", "Ratings"]]
