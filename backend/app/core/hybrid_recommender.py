import pandas as pd
import pickle
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === Path Setup ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")  
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

# Correct the file names here
RATINGS_PATH = os.path.join(DATA_DIR, "cleaned_ratings_data.csv")  
DESTINATIONS_PATH = os.path.join(DATA_DIR, "cleaned_feature_hybrid_dataset.csv")  
MODEL_PATH = os.path.join(MODELS_DIR, "svd_model.pkl")  
RECOMMENDATION_HISTORY_FILE = os.path.join(DATA_DIR, "recommendation_history.csv")  

# === Load Data ===
print(f"Data directory: {DATA_DIR}")
print(f"Ratings file path: {RATINGS_PATH}")
ratings_df = pd.read_csv(RATINGS_PATH)
destinations_df = pd.read_csv(DESTINATIONS_PATH)

# === Load Collaborative Filtering Model ===
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"SVD model not found at {MODEL_PATH}")

with open(MODEL_PATH, "rb") as f:
    svd_model = pickle.load(f)

# === Hybrid Recommender ===
def hybrid_recommend(user_id, budget, weather=None, activities=None, accommodation_type=None, top_n=10):
    filtered_df = destinations_df.copy()

    # Weather filter
    if "weather" in filtered_df.columns and weather:
        filtered_df = filtered_df[filtered_df["weather"].str.lower() == weather.lower()]
    elif weather:
        print("Weather column not found, skipping weather filter.")

    # Activities filter
    if "activities" in filtered_df.columns and activities:
        activity_list = [a.strip().lower() for a in activities.split(",")]
        filtered_df = filtered_df[filtered_df["activities"].apply(lambda x: any(act in str(x).lower() for act in activity_list))]
    elif activities:
        print("Activities column not found, skipping activities filter.")

    # Accommodation type filter
    if accommodation_type:
        if "accommodation_type" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["accommodation_type"].str.lower() == accommodation_type.lower()]
        else:
            print("Accommodation type column not found, skipping filter.")

    # Budget filter
    filtered_df = filtered_df[filtered_df["price"] <= budget]

    # Exclude items already rated by user
    user_items = ratings_df[ratings_df["user_id"] == user_id]["item_id"].unique()
    filtered_df = filtered_df[~filtered_df["item_id"].isin(user_items)]

    if filtered_df.empty:
        return {"message": "No recommendations found based on provided filters."}

    # Collaborative Filtering
    if len(user_items) > 0:
        try:
            filtered_df["predicted_rating"] = filtered_df["item_id"].apply(
                lambda item_id: svd_model.predict(user_id, item_id).est
            )
            sorted_df = filtered_df.sort_values(by="predicted_rating", ascending=False)
        except Exception as e:
            print("⚠️ Collaborative filtering failed:", e)
            sorted_df = filtered_df
    else:
        # Fallback to content-based
        sorted_df = fallback_content_based(activities, budget, top_n)

    # Top N
    top_recommendations = sorted_df.head(top_n).to_dict(orient="records")
    save_recommendation_history(user_id, top_recommendations)

    return top_recommendations

# === Content-Based Fallback ===
def fallback_content_based(activities, budget, top_n):
    tfidf = TfidfVectorizer(stop_words="english")

    if "activities" in destinations_df.columns:
        text_column = destinations_df["activities"].fillna("")
    elif "destination_name" in destinations_df.columns:
        print("Fallback to 'destination_name' as 'activities' is missing.")
        text_column = destinations_df["destination_name"].fillna("")
    else:
        raise ValueError("No suitable text column (activities or destination_name) found.")

    tfidf_matrix = tfidf.fit_transform(text_column)
    activity_query = " ".join(activities.split(",")) if activities else ""
    query_vec = tfidf.transform([activity_query])
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()

    destinations_df["similarity"] = cosine_sim
    fallback_df = destinations_df[destinations_df["price"] <= budget]

    return fallback_df.sort_values(by="similarity", ascending=False)

# === Recommendation History ===
def save_recommendation_history(user_id, recommendations):
    records = []

    for rec in recommendations:
        records.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "item_id": rec.get("item_id"),
            "destination_name": rec.get("destination_name", ""),
            "predicted_rating": rec.get("predicted_rating", None)
        })

    history_df = pd.DataFrame(records)

    if os.path.exists(RECOMMENDATION_HISTORY_FILE):
        existing_df = pd.read_csv(RECOMMENDATION_HISTORY_FILE)
        combined_df = pd.concat([existing_df, history_df], ignore_index=True)
    else:
        combined_df = history_df

    combined_df.to_csv(RECOMMENDATION_HISTORY_FILE, index=False)

# === Public API ===
def recommend_items(user_id, budget, weather=None, activities=None, accommodation_type=None, top_n=10):
    return hybrid_recommend(user_id, budget, weather, activities, accommodation_type, top_n)

# === Test the Recommendation Function ===

# Example test inputs
user_id = 1  
budget = 500  

# Optional filters (remove or modify these as needed)
weather = "hot" 
activities = "beach"  
accommodation_type = "hotel" 

# Call the recommend_items function to generate recommendations
recommendations = recommend_items(user_id, budget, weather, activities, accommodation_type)

# Print the output (recommendations)
print("Recommendations:", recommendations)

# Optionally print the first recommendation in detail
if recommendations:
    print("First Recommendation:", recommendations[0])
else:
    print("No recommendations found.")
