# analysis_and_report.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from surprise import SVD, KNNBasic, Dataset, Reader
from surprise.model_selection import train_test_split, GridSearchCV, cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np
import json

# === Output folders ===
os.makedirs("report_images", exist_ok=True)
os.makedirs("report_logs", exist_ok=True)

# === Load data ===
ratings = pd.read_csv("ml-latest-small/ratings.csv")
movies = pd.read_csv("ml-latest-small/movies.csv")
tags = pd.read_csv("ml-latest-small/tags.csv")

# === Plot 1: Ratings Distribution ===
plt.figure(figsize=(8, 5))
sns.histplot(ratings['rating'], bins=10, kde=True, color='skyblue')
plt.title("Ratings Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.savefig("report_images/ratings_distribution.png")
plt.close()

# === Plot 2: Genre Frequency ===
genre_counts = pd.Series(" | ".join(movies['genres']).split("|")).value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="viridis")
plt.title("Genre Frequency")
plt.xlabel("Count")
plt.savefig("report_images/genre_frequency.png")
plt.close()

# === Feature Analysis: TF-IDF Visualization ===
tag_data = tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()
movies_with_tags = pd.merge(movies, tag_data, on='movieId', how='left')
movies_with_tags['tag'] = movies_with_tags['tag'].fillna('')
movies_with_tags['metadata'] = movies_with_tags['genres'].str.replace("|", " ") + " " + movies_with_tags['tag']

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_with_tags['metadata'])
svd = TruncatedSVD(n_components=2)
reduced = svd.fit_transform(tfidf_matrix)

plt.figure(figsize=(8, 6))
plt.scatter(reduced[:, 0], reduced[:, 1], alpha=0.4, s=10)
plt.title("TF-IDF Metadata Feature Projection (2D)")
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.savefig("report_images/tfidf_2d_projection.png")
plt.close()

# === Prepare Surprise Dataset ===
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# === Model Comparison ===
models = {
    "SVD": SVD(),
    "KNNBasic": KNNBasic()
}

comparison_results = {}
for name, model in models.items():
    results = cross_validate(model, data, measures=['RMSE', 'MAE'], cv=3, verbose=False)
    comparison_results[name] = {
        "RMSE": np.mean(results['test_rmse']),
        "MAE": np.mean(results['test_mae'])
    }

with open("report_logs/model_comparison.json", "w") as f:
    json.dump(comparison_results, f, indent=2)

# === Hyperparameter Tuning ===
param_grid = {
    "n_factors": [50, 100],
    "reg_all": [0.02, 0.05]
}
gs = GridSearchCV(SVD, param_grid, measures=["rmse"], cv=3)
gs.fit(data)

best_params = gs.best_params['rmse']
best_score = gs.best_score['rmse']

with open("report_logs/best_hyperparameters.json", "w") as f:
    json.dump({
        "best_params": best_params,
        "best_score_rmse": best_score
    }, f, indent=2)

print("✅ Analysis complete. Check `report_images/` and `report_logs/`.")
