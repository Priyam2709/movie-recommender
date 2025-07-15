import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import SVDpp, Dataset, Reader
from surprise.model_selection import train_test_split
import requests


# === TMDb Poster Setup ===
# TMDB_API_KEY = "9b5eea108360f410aa29d53ffe3a5ed9"  # Replace this with your actual API key
# poster_cache = {}

# def get_tmdb_poster(title):
#     if title in poster_cache:
#         return poster_cache[title]

#     try:
#         response = requests.get(
#             "https://api.themoviedb.org/3/search/movie",
#             params={"api_key": TMDB_API_KEY, "query": title},
#         )
#         data = response.json()
#         results = data.get("results")
#         if results:
#             poster_path = results[0].get("poster_path")
#             if poster_path:
#                 full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
#                 poster_cache[title] = full_url
#                 return full_url
#     except Exception as e:
#         print(f"Error fetching poster for {title}: {e}")

# === Load datasets ===
ratings = pd.read_csv("ml-latest-small/ratings.csv")
movies = pd.read_csv("ml-latest-small/movies.csv")
tags = pd.read_csv("ml-latest-small/tags.csv")
links = pd.read_csv("ml-latest-small/links.csv")
links['imdbId'] = links['imdbId'].astype(str).str.zfill(7)  # ensure 7-digit IMDb ID

# Merge IMDb ID into movies dataframe
movies_with_links = pd.merge(movies, links[['movieId', 'imdbId']], on='movieId', how='left')

OMDB_API_KEY = "8bf5ae80"

def get_omdb_poster_by_imdb(imdb_id):
    if pd.isna(imdb_id):
        return None

    imdb_id = str(int(imdb_id)).zfill(7)  # Ensure it's 7-digit like '0114709'
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i=tt{imdb_id}"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("Poster") if data.get("Poster") != "N/A" else None
    except:
        return None

    # fallback = "https://via.placeholder.com/500x750?text=No+Poster"
    # poster_cache[title] = fallback
    # return fallback

def extract_year(title):
    if '(' in title and ')' in title:
        try:
            return title.split('(')[-1].split(')')[0]
        except:
            return "N/A"
    return "N/A"



# === Combine metadata ===
tag_data = tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()
movies_with_tags = pd.merge(movies, tag_data, on='movieId', how='left')
movies_with_tags['tag'] = movies_with_tags['tag'].fillna('')
movies_with_tags['genres'] = movies_with_tags['genres'].str.replace('|', ' ', regex=False)
movies_with_tags['metadata'] = movies_with_tags['genres'] + ' ' + movies_with_tags['tag']

# === TF-IDF and Cosine Similarity ===
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_with_tags['metadata'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# === Collaborative Filtering Model (SVD++) ===
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
trainset, _ = train_test_split(data, test_size=0.2, random_state=42)

svd_model = SVDpp()
svd_model.fit(trainset)

# === Expose global objects ===
all_ratings = ratings
all_movies = movies_with_links
cosine_matrix = cosine_sim
svdpp = svd_model

# === Helper functions ===

def get_user_positive_movies(user_id, ratings_df, threshold=4.0):
    return ratings_df[(ratings_df['userId'] == user_id) & (ratings_df['rating'] >= threshold)]['movieId'].tolist()

def get_similar_movies_from_content(movie_ids, movies_df, cosine_sim, top_n=5):
    indices = pd.Series(movies_df.index, index=movies_df['movieId'])
    similar_ids = set()

    for movie_id in movie_ids:
        if movie_id not in indices:
            continue
        idx = indices[movie_id]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        similar_ids.update([movies_df.iloc[i[0]]['movieId'] for i in sim_scores])

    return list(similar_ids)

def rank_by_svdpp(user_id, movie_ids, svd_model, movies_df, top_n=10):
    ranked = []
    for movie_id in movie_ids:
        pred = svd_model.predict(user_id, movie_id)
        ranked.append((movie_id, pred.est))

    ranked.sort(key=lambda x: x[1], reverse=True)
    results = []
    for movie_id, est_rating in ranked[:top_n]:
        movie = movies_df[movies_df['movieId'] == movie_id][['title', 'genres']].iloc[0]
        results.append({
            'title': movie['title'],
            'genre': movie['genres'],
            'predicted_rating': round(est_rating, 2),
            'poster': get_omdb_poster_by_imdb(movie['imbdId']),
            'year': extract_year(movie['title'])
        })

    return pd.DataFrame(results)

# === Main recommendation function ===
def recommend(
    user_id,
    ratings_df=all_ratings,
    movies_df=all_movies,
    cosine_sim=cosine_matrix,
    svd_model=svdpp,
    top_n=10
):
    liked_movie_ids = get_user_positive_movies(user_id, ratings_df)

    if not liked_movie_ids:
        return f"No high-rated history for user {user_id}"

    content_based_ids = get_similar_movies_from_content(liked_movie_ids, movies_df, cosine_sim)
    recommendations = rank_by_svdpp(user_id, content_based_ids, svd_model, movies_df, top_n)
    return recommendations

default_movies_df = all_movies
