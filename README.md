# 🎬 Movie Recommender System (Swipe-based)

An interactive Movie Recommendation System powered by **Content-Based Filtering (TF-IDF + Cosine Similarity)** and **Collaborative Filtering (SVD++)**, with a fun **swipe-based UI** built in **React (Framer Motion)** and a **FastAPI backend**.

---

## 📂 Project Structure

```
├── movie-recommender-backend/
│   ├── ml-latest-small/       # Datasets (ratings, movies, tags)
│   ├── main.py                # FastAPI Backend API
│   ├── recommender_model.py   # Recommendation Models (TF-IDF, Cosine, SVD++)
│   ├── analysis_and_report.py # Data Analysis, Visualization, Reporting Script
│   ├── report_images/         # Generated Graphs and Charts
│   ├── report_logs/           # Logs of Model Evaluation
│   ├── swipes.json            # Stored User Swipe History
│   └── requirements.txt       # Python Dependencies
│
├── movie-recommender-frontend/
│   ├── src/
│   │   ├── App.js             # React Entry
│   │   ├── MovieSwipe.js      # Swipe UI (Framer Motion)
│   ├── package.json           # React Dependencies
│   ├── tailwind.config.js     # TailwindCSS Config
│   └── ...etc
```

---

## 🛠️ Features

✅ Swipe left (dislike) / right (like)
✅ Auto-updating recommendations
✅ Saved user swipe history
✅ Reset history button
✅ Fallback recommendations if history is empty
✅ TMDb Poster Integration
✅ Interactive Data Analysis with saved visual reports
✅ FastAPI + React integration
✅ Ready for GitHub deployment

---

## 🔍 Key Components (as per academic/project requirements)

| Requirement               | Status                                                              |
| ------------------------- | ------------------------------------------------------------------- |
| **Data Visualization**    | ✅ `analysis_and_report.py` + `report_images/`                       |
| **Feature Analysis**      | ✅ Genres, Tags via TF-IDF                                           |
| **Model Building**        | ✅ SVD++ (Collaborative), TF-IDF + Cosine Similarity (Content-based) |
| **Hyperparameter Tuning** | ✅ In `analysis_and_report.py`                                       |
| **Model Comparison**      | ✅ SVD vs KNN vs Random Baseline                                     |
| **Deployment**            | ✅ FastAPI (Backend), React (Frontend)                               |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/yourusername/movie-recommender.git
cd A/movie-recommender-backend
```

### 2️⃣ Backend Setup

```bash
# Activate your Python environment
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload
```

---

### 3️⃣ Frontend Setup

```bash
cd ../movie-recommender-frontend
npm install
npm run dev
```

---

## 📊 Analysis & Reporting

Run this Python script to generate:

* Data exploration plots
* Feature importance
* Model comparison (SVD, KNN)
* Evaluation logs and images saved

```bash
python analysis_and_report.py
```

Results saved in:
`/report_images` and `/report_logs`

---

## 🎯 Example APIs (Backend)

| Endpoint                | Method | Purpose             |
| ----------------------- | ------ | ------------------- |
| `/recommend/{user_id}`  | GET    | Get recommendations |
| `/swipe/`               | POST   | Save swipe          |
| `/swipe-history`        | GET    | Fetch swipe history |
| `/reset-history/{user}` | DELETE | Reset user history  |

---

## 🖥️ Tech Stack

| Frontend                         | Backend | ML / Recsys                         | Visualization       |
| -------------------------------- | ------- | ----------------------------------- | ------------------- |
| React + Tailwind + Framer Motion | FastAPI | Surprise SVD++, Scikit-Learn TF-IDF | Matplotlib, Seaborn |

---

## 💡 Future Improvements

* User Authentication
* Real Movie Posters from TMDb API
* Enhanced collaborative model (Neural CF)
* Cloud deployment (Render / Vercel)

---

## 👩‍💻 Made by Priyam Saxena , Kadambala Likhith , Sayan Mondal 
