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

# === Hybrid Recommendation with Filters ===

def hybrid_recommend(user_id, budget, weather=None, activities=None, accommodation_type=None, destination=None, top_n=10):
    # Step 1: Filter destinations based on weather, activities, accommodation type, and destination
    filtered_df = destinations_df.copy()

    # Check if 'weather' column exists, and apply weather filter if provided
    if 'weather' in filtered_df.columns and weather:
        filtered_df = filtered_df[filtered_df["weather"].str.lower() == weather.lower()]
    elif 'weather' not in filtered_df.columns:
        print("Weather column not found, skipping weather filter.")

    # Check if 'activities' column exists, and apply activities filter if provided
    if 'activities' in filtered_df.columns and activities:
        activity_list = [a.strip().lower() for a in activities.split(",")]
        filtered_df = filtered_df[filtered_df["activities"].apply(
            lambda x: any(act in str(x).lower() for act in activity_list)
        )]
    elif 'activities' not in filtered_df.columns:
        print("Activities column not found, skipping activities filter.")

    # Check if 'accommodation_type' column exists and apply filter
    if accommodation_type:
        if 'accommodation_type' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["accommodation_type"].str.lower() == accommodation_type.lower()]
        else:
            print("Accommodation type column not found, skipping accommodation filter.")

    # **New Step: Apply destination filter if provided**
    if destination:
        if 'destination' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["destination"].str.lower() == destination.lower()]
        else:
            print("Destination column not found, skipping destination filter.")

    # Step 2: Apply budget filter
    filtered_df = filtered_df[filtered_df["price"] <= budget]

    # Step 3: Exclude items the user has already interacted with
    user_items = interactions_df[interactions_df["user_id"] == user_id]["item_id"].unique()
    filtered_df = filtered_df[~filtered_df["item_id"].isin(user_items)]

    if filtered_df.empty:
        return {"message": "No recommendations found based on filters."}

    # Step 4: Apply collaborative filtering (SVD) if there are user interactions
    if len(user_items) > 0:
        try:
            filtered_df["predicted_rating"] = filtered_df["item_id"].apply(
                lambda item_id: svd_model.predict(user_id, item_id).est
            )
            sorted_df = filtered_df.sort_values(by="predicted_rating", ascending=False)
        except Exception:
            sorted_df = filtered_df
    else:
        # Fallback to content-based recommendations if no prior interactions exist
        sorted_df = fallback_content_based(activities, budget, top_n)

    # Step 5: Get top N recommendations
    top_recommendations = sorted_df.head(top_n).to_dict(orient="records")

    # Save the recommendation history
    save_recommendation_history(user_id, top_recommendations)

    return top_recommendations


# === Fallback Content-Based Recommendation ===

def fallback_content_based(activities, budget, top_n):
    # Handle case where 'activities' column might be missing
    if 'activities' not in destinations_df.columns:
        print("Activities column not found, fallback based on other features.")
        # Fallback strategy based on other features, e.g., using a default string or the item name
        tfidf = TfidfVectorizer(stop_words='english')
        # Use 'destination' instead of 'destination_name'
        tfidf_matrix = tfidf.fit_transform(destinations_df["destination"].fillna(""))

        # Build a query vector from the activities input, even if activities is missing
        activity_query = " ".join(activities.split(",")) if activities else ""
        query_vec = tfidf.transform([activity_query])

        cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
        destinations_df["similarity"] = cosine_sim

        # Filter by budget
        fallback_df = destinations_df[destinations_df["price"] <= budget]
        return fallback_df.sort_values(by="similarity", ascending=False)
    else:
        # Proceed with the normal fallback content-based strategy
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(destinations_df["activities"].fillna(""))

        # Build a query vector from the activities input
        activity_query = " ".join(activities.split(",")) if activities else ""
        query_vec = tfidf.transform([activity_query])

        cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
        destinations_df["similarity"] = cosine_sim

        # Filter by budget
        fallback_df = destinations_df[destinations_df["price"] <= budget]
        return fallback_df.sort_values(by="similarity", ascending=False)


# === Save Recommendation History ===

def save_recommendation_history(user_id, recommendations):
    history_records = []

    for rec in recommendations:
        history_records.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "item_id": rec.get("item_id"),
            "destination": rec.get("destination", ""),
            "predicted_rating": rec.get("predicted_rating", None)
        })

    history_df = pd.DataFrame(history_records)

    if os.path.exists(RECOMMENDATION_HISTORY_FILE):
        existing_df = pd.read_csv(RECOMMENDATION_HISTORY_FILE)
        combined_df = pd.concat([existing_df, history_df], ignore_index=True)
    else:
        combined_df = history_df

    combined_df.to_csv(RECOMMENDATION_HISTORY_FILE, index=False)




