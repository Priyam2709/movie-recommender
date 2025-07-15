from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import json
import os
import random
import pandas as pd
from recommender_model import svdpp, all_ratings, all_movies, cosine_matrix, recommend, default_movies_df
from fastapi.middleware.cors import CORSMiddleware
from recommender_model import get_omdb_poster_by_imdb


app = FastAPI()

# ✅ CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SWIPE_FILE = "swipes.json"

class SwipeData(BaseModel):
    user_id: int
    movie_title: str
    action: str

@app.post("/swipe/")
def save_swipe(data: SwipeData):
    history = {}
    if os.path.exists(SWIPE_FILE):
        with open(SWIPE_FILE, "r") as f:
            history = json.load(f)
    history.setdefault(str(data.user_id), []).append({
        "movie_title": data.movie_title,
        "action": data.action
    })
    with open(SWIPE_FILE, "w") as f:
        json.dump(history, f, indent=2)
    return {"message": "Swipe saved"}

@app.get("/swipe-history")
def get_swipe_history(user_id: int):
    if not os.path.exists(SWIPE_FILE):
        return {"history": []}
    with open(SWIPE_FILE, "r") as f:
        history = json.load(f)
    return {"history": history.get(str(user_id), [])}

@app.get("/recommend/{user_id}")
@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int):
    if not os.path.exists(SWIPE_FILE):
        return {"recommendations": [], "note": "No swipe file found"}

    with open(SWIPE_FILE, "r") as f:
        history = json.load(f)

    swipes = history.get(str(user_id), [])
    swiped_titles = [s["movie_title"].strip().lower() for s in swipes if s["action"] == "like"]

    title_map = {title.lower(): title for title in all_movies['title'].tolist()}
    matched_titles = [title_map.get(t) for t in swiped_titles if t in title_map]
    matched_titles = [t for t in matched_titles if t]

    liked_movie_ids = all_movies[all_movies['title'].isin(matched_titles)]['movieId'].tolist()

    if not liked_movie_ids:
        fallback_sample = default_movies_df.sample(10, random_state=random.randint(1, 1000))
        fallback_sample = fallback_sample[['title', 'genres']].copy()
        fallback_sample['poster'] = "https://via.placeholder.com/300x450?text=Movie"
        fallback_sample['year'] = "N/A"
        return {
            "recommendations": fallback_sample.to_dict(orient="records"),
            "note": "Fallback used: No liked movies matched our dataset."
        }

    indices = pd.Series(all_movies.index, index=all_movies['movieId'])
    all_swiped = set(s["movie_title"].strip().lower() for s in swipes)
    similar_ids = set()

    for movie_id in liked_movie_ids:
        if movie_id in indices:
            idx = indices[movie_id]
            sim_scores = sorted(list(enumerate(cosine_matrix[idx])), key=lambda x: x[1], reverse=True)[1:20]
            similar_ids.update(all_movies.iloc[i[0]]['movieId'] for i in sim_scores)

    results = []
    for movie_id in similar_ids:
        row = all_movies[all_movies['movieId'] == movie_id].iloc[0]
        title_lower = row['title'].strip().lower()
        if title_lower in all_swiped:
            continue
        pred = svdpp.predict(user_id, movie_id).est
        results.append({
            "title": row['title'],
            "genre": row['genres'],
            "year": "N/A",
            "poster": get_omdb_poster_by_imdb(row['imdbId']),
            "predicted_rating": round(pred, 2)
        })

    sorted_results = sorted(results, key=lambda x: x['predicted_rating'], reverse=True)

    return {
        "recommendations": sorted_results[:10],
        "note": "Recommendations generated from your swipes!"
    }
from fastapi.responses import JSONResponse

@app.delete("/reset-history/{user_id}")
def reset_history(user_id: int):
    if not os.path.exists(SWIPE_FILE):
        return {"message": "No swipe history to delete."}

    with open(SWIPE_FILE, "r") as f:
        history = json.load(f)

    history[str(user_id)] = []

    with open(SWIPE_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return JSONResponse(content={"message": "History reset successfully."})
