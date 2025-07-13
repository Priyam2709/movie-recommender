
# 🎬 AI-Powered Movie Recommender

An AI-based movie recommendation system with a swipe interface built using **React + FastAPI**. Users swipe to like/dislike movies, and the system dynamically learns preferences to provide personalized recommendations using a hybrid of **Collaborative Filtering (SVD++)** and **Content-Based Filtering (TF-IDF + Cosine Similarity)**.

![screenshot](https://via.placeholder.com/800x450.png?text=Demo+Screenshot)

## 🚀 Features

✅ Swipe left (dislike) / right (like)  
✅ Personalized recommendations based on user swipes  
✅ Real-time recommendations using SVD++ and genre-tag similarity  
✅ Posters and year fetched using TMDb API  
✅ Reset user history  
✅ Works locally without login  
✅ Clean, mobile-friendly UI

## 🛠️ Tech Stack

| Layer      | Technology            |
|-----------|------------------------|
| Frontend  | React, Tailwind CSS, Framer Motion |
| Backend   | FastAPI, Python        |
| ML Models | Surprise SVD++, TF-IDF |
| Data      | MovieLens `ml-latest-small` |
| API       | [TMDb](https://www.themoviedb.org/documentation/api) for movie posters |

## 🧠 Recommendation Engine

### 🎯 Hybrid Model

1. **Content-Based Filtering**  
   - Uses `genres + tags` processed via `TfidfVectorizer`  
   - Computes movie similarity using cosine similarity

2. **Collaborative Filtering**  
   - Uses `SVD++` from `surprise` library  
   - Predicts personalized rating estimates per user

3. **Fusion**  
   - For each liked movie → get top 5 similar movies  
   - Predict ratings for those using SVD++  
   - Return top 10 predicted movies

## 📁 Folder Structure

```
movie-recommender/
│
├── movie-swipe-framer(frontend)/                     # React Frontend
│   ├── public/
│   ├── src/
│   │   └── MovieSwipe.js         # Main UI Component
│   └── ...
│
├── movie-recommender-backend(backend)/                      # FastAPI Backend
│   ├── main.py                   # FastAPI server
│   ├── recommender_model.py      # ML recommendation engine
│   ├── swipes.json               # Swipe history storage
│   └── ml-latest-small/          # MovieLens dataset
│       ├── movies.csv
│       ├── ratings.csv
│       └── tags.csv
```

## 🧪 Setup Instructions

### 1. 📦 Backend Setup (Python 3.10 recommended)

```bash
cd movie-recommender-backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, use:

```bash
pip install fastapi uvicorn pandas scikit-learn scikit-surprise requests
```

### 2. ✅ Run Backend

```bash
uvicorn main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### 3. 💻 Frontend Setup

```bash
cd movie-swipe-framer
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

## 🔑 TMDb API Setup (for posters)

1. Sign up at https://www.themoviedb.org
2. Go to [API settings](https://www.themoviedb.org/settings/api)
3. Copy your **API key (v3 auth)**  
4. In `recommender_model.py`, set:

```python
TMDB_API_KEY = "your_api_key_here"
```

## 🔁 Endpoints (Backend)

| Method | Endpoint                 | Description                      |
|--------|--------------------------|----------------------------------|
| `GET`  | `/recommend/{user_id}`   | Get top movie recommendations   |
| `POST` | `/swipe/`                | Save like/dislike for a movie   |
| `GET`  | `/swipe-history`         | Get history for a user          |
| `DELETE` | `/reset-history/{user_id}` | Reset user swipe history     |

## 🖼 Sample Movie Object Returned

```json
{
  "title": "The Matrix",
  "genre": "Action Sci-Fi",
  "year": "1999",
  "poster": "https://image.tmdb.org/t/p/w500/abcd1234.jpg",
  "predicted_rating": 4.76
}
```

## 📌 Notes

- Recommendation logic is in `recommender_model.py`
- Poster fetching is cached in `poster_cache` for speed
- Swipe data is stored in `swipes.json` (consider switching to a database for production)

## 📸 Demo

> Coming soon: video/gif demo link or screenshots

## 📚 Credits

- MovieLens dataset: https://grouplens.org/datasets/movielens/
- TMDb API: https://www.themoviedb.org/
- Surprise SVD++: https://surpriselib.com/

## 📄 License

MIT License.  
Use for educational and personal projects.

Awesome! Here's everything you need to **document and present your `analysis_and_report.py` module** professionally — perfect for your project submission or GitHub:

---

## ✅ README Section for `analysis_and_report.py`

You can **add this to your existing README.md**:

---

### 📊 Analysis & Reporting Module

The `analysis_and_report.py` script provides comprehensive model analysis and visual reporting for the recommender system. It complements the deployed app by documenting performance and insights using saved images and logs.

#### 💡 Features:

* **Data Visualization**: Heatmaps, distribution plots, and rating counts.
* **Feature Analysis**: Correlation matrix and rating patterns.
* **Model Building**: Uses both `SVD` and `KNNBasic` from `Surprise`.
* **Hyperparameter Tuning**: Uses `GridSearchCV` to find optimal settings.
* **Model Comparison**: Evaluates RMSE of different models on the same dataset.
* **Reporting**: Saves visual plots and a `report.log` for offline reporting.

---

#### 📁 Outputs Saved To:

| Type           | Location                           |
| -------------- | ---------------------------------- |
| Visualizations | `outputs/*.png`                    |
| Log File       | `outputs/report.log`               |
| Tuning Results | Printed in terminal & saved in log |

---

#### ▶️ To Run:

```bash
python analysis_and_report.py
```

Ensure you have these dependencies installed:

```bash
pip install matplotlib seaborn scikit-learn scikit-surprise
```

---

## 🗂 Folder Structure (Example)

```
movie-recommender-backend/
├── main.py
├── recommender_model.py
├── analysis_and_report.py   <-- 🔍 Analysis script
├── outputs/                 <-- 📊 Visual charts and log files
│   ├── rating_distribution.png
│   ├── correlation_heatmap.png
│   ├── svd_vs_knn_rmse.png
│   └── report.log
├── ml-latest-small/
│   ├── ratings.csv
│   ├── movies.csv
│   └── tags.csv
```

---

## 📄 Sample report.log (snippet)

```
--- FEATURE ANALYSIS ---
Most rated movie: Forrest Gump (1994)
User with most ratings: ID 414
...

--- MODEL COMPARISON ---
SVD RMSE: 0.8734
KNN RMSE: 0.9431
Best model: SVD
...
```

