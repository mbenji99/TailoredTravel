import pandas as pd
import pickle
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get absolute base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

INTERACTIONS_PATH = os.path.join(DATA_DIR, "cleaned_interactions.csv")
DESTINATIONS_PATH = os.path.join(DATA_DIR, "cleaned_feature_hybrid_dataset.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "svd_model.pkl")
RECOMMENDATION_HISTORY_FILE = os.path.join(DATA_DIR, "recommendation_history.csv")

# Load data
interactions_df = pd.read_csv(INTERACTIONS_PATH)
destinations_df = pd.read_csv(DESTINATIONS_PATH)

# Load trained SVD model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Trained collaborative filtering model not found at: {MODEL_PATH}")

with open(MODEL_PATH, "rb") as f:
    svd_model = pickle.load(f)


def recommend_items(user_id, budget, weather=None, environment=None, activities=None, top_n=10):
    user_items = interactions_df[interactions_df["user_id"] == user_id]["item_id"].unique()
    filtered_df = destinations_df.copy()

    if weather:
        filtered_df = filtered_df[filtered_df["weather"].str.lower() == weather.lower()]
    if environment:
        filtered_df = filtered_df[filtered_df["environment"].str.lower() == environment.lower()]
    if activities:
        activity_list = [a.strip().lower() for a in activities.split(",")]
        filtered_df = filtered_df[
            filtered_df["activities"].apply(
                lambda x: any(act in str(x).lower() for act in activity_list)
            )
        ]

    filtered_df = filtered_df[filtered_df["price"] <= budget]
    filtered_df = filtered_df[~filtered_df["item_id"].isin(user_items)]

    if filtered_df.empty:
        return {"message": "No recommendations found based on filters."}

    if len(user_items) > 0:
        try:
            filtered_df["predicted_rating"] = filtered_df["item_id"].apply(
                lambda item_id: svd_model.predict(user_id, item_id).est
            )
            sorted_df = filtered_df.sort_values(by="predicted_rating", ascending=False)
        except Exception:
            sorted_df = filtered_df
    else:
        sorted_df = fallback_content_based(activities, budget, top_n)

    top_recommendations = sorted_df.head(top_n).to_dict(orient="records")
    save_recommendation_history(user_id, top_recommendations)

    return top_recommendations


def fallback_content_based(activities, budget, top_n):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(destinations_df["activities"].fillna(""))

    activity_query = " ".join(activities.split(",")) if activities else ""
    query_vec = tfidf.transform([activity_query])

    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    destinations_df["similarity"] = cosine_sim

    fallback_df = destinations_df[destinations_df["price"] <= budget]
    return fallback_df.sort_values(by="similarity", ascending=False)


def save_recommendation_history(user_id, recommendations):
    history_records = []

    for rec in recommendations:
        history_records.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "item_id": rec.get("item_id"),
            "destination_name": rec.get("destination_name", ""),
            "predicted_rating": rec.get("predicted_rating", None)
        })

    history_df = pd.DataFrame(history_records)

    if os.path.exists(RECOMMENDATION_HISTORY_FILE):
        existing_df = pd.read_csv(RECOMMENDATION_HISTORY_FILE)
        combined_df = pd.concat([existing_df, history_df], ignore_index=True)
    else:
        combined_df = history_df

    combined_df.to_csv(RECOMMENDATION_HISTORY_FILE, index=False)
