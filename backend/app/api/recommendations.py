from flask import Blueprint, request, jsonify
from pathlib import Path
import pandas as pd

from app.core.hybrid_recommender import hybrid_recommend
from app.recommenders.collaborative_filtering import get_cf_recommendations
from app.recommenders.content_based_filtering import get_cb_recommendations
from app.recommenders.clustering_model import get_user_cluster_recommendations
from app.recommenders.cf_model import load_cf_model
from app.recommenders.content_model import load_cb_model
from app.recommenders.clustering_model import load_clustering_model

# Load models
cf_model = load_cf_model('models/cf_model.h5')
clustering_model = load_clustering_model('models/clustering_model.pkl')

model_path = Path(__file__).resolve().parent.parent / 'models' / 'content_based_model.pkl'
cb_data = load_cb_model(model_path)

# Use dictionary keys
cb_model = cb_data["tfidf_model"]
cb_matrix = cb_data["tfidf_matrix"]
cb_items_df = cb_data["hotels_df"]

interactions_df = pd.read_csv('data/cleaned_interactions.csv')
user_feats_df = pd.read_csv('data/user_features.csv')

# Set up Flask blueprint
recommendations_bp = Blueprint('recommendations', __name__)

# Collaborative Filtering recommendations
@recommendations_bp.route("/cf", methods=["POST"])
def cf_recommendations():
    data = request.get_json()
    user_id = data.get("user_id")
    num_recommendations = data.get("num_recommendations", 10)
    
    try:
        recommendations = get_cf_recommendations(user_id, num_recommendations, cf_model, interactions_df)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": f"CF Recommendation error: {str(e)}"}), 500

# Content-Based Filtering recommendations
@recommendations_bp.route("/cb", methods=["POST"])
def cb_recommendations():
    data = request.get_json()
    hotel_id = data.get("hotel_id")
    num_recommendations = data.get("num_recommendations", 10)
    
    try:
        recommendations = get_cb_recommendations(hotel_id, num_recommendations, cb_matrix, cb_items_df)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": f"CB Recommendation error: {str(e)}"}), 500

# Cluster-based recommendations
@recommendations_bp.route("/cluster", methods=["POST"])
def cluster_recommendations():
    data = request.get_json()
    user_id = data.get("user_id")
    num_recommendations = data.get("num_recommendations", 10)
    
    try:
        recommendations = get_user_cluster_recommendations(user_id, num_recommendations, clustering_model, user_feats_df)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": f"Cluster Recommendation error: {str(e)}"}), 500

# Hybrid Recommendations
@recommendations_bp.route("/hybrid", methods=["OPTIONS", "POST"])
def hybrid_recommendations():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()

    # Extract preferences from request, with default fallback if missing
    user_id = data.get("user_id", 1)  
    top_n = data.get("top_n", 5)      
    weather = data.get("weather", None)
    activities = data.get("activities", None)
    accommodation_type = data.get("accommodation_type", None)
    budget = data.get("budget", None)  

    try:
        print(f"Filtering data with preferences: weather={weather}, activities={activities}, accommodation_type={accommodation_type}, budget={budget}")
        
        # Call the hybrid recommender function with the user preferences
        recommendations = hybrid_recommend(
            user_id=user_id,
            top_n=top_n,
            weather=weather,
            activities=activities,
            accommodation_type=accommodation_type,
            budget=budget  
        )

        # Check if the recommendations list is empty
        if not recommendations:
            print("No recommendations found based on the given preferences, providing fallback recommendations.")
            recommendations = ["Default Recommendation 1", "Default Recommendation 2"]

        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": f"Hybrid Recommendation error: {str(e)}"}), 500
