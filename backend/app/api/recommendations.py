from flask import Blueprint, request, jsonify
from pathlib import Path
import pandas as pd

from app.core.hybrid_recommender import get_hybrid_recommendations
from app.recommenders.collaborative_filtering import get_cf_recommendations
from app.recommenders.content_based_filtering import get_cb_recommendations
from app.recommenders.clustering_model import get_user_cluster_recommendations
from app.recommenders.cf_model import load_cf_model
from app.recommenders.content_model import load_cb_model
from app.recommenders.clustering_model import load_clustering_model

cf_model = load_cf_model('models/cf_model.h5')
clustering_model = load_clustering_model('models/clustering_model.pkl')

model_path = Path(__file__).resolve().parent.parent / 'models' / 'content_based_model.pkl'
cb_data = load_cb_model(model_path)

# ✅ Use dictionary keys
cb_model = cb_data["tfidf_model"]
cb_matrix = cb_data["tfidf_matrix"]
cb_items_df = cb_data["hotels_df"]

interactions_df = pd.read_csv('data/cleaned_interactions.csv')
user_feats_df = pd.read_csv('data/user_features.csv')

recommendations_bp = Blueprint('recommendations', __name__)

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

@recommendations_bp.route("/hybrid", methods=["POST"])
def hybrid_recommendations():
    data = request.get_json()
    user_id = data.get("user_id")
    num_recommendations = data.get("num_recommendations", 10)
    try:
        recommendations = get_hybrid_recommendations(
            user_id=user_id,
            num_recommendations=num_recommendations,
            cf_model=cf_model,
            cb_model=cb_model,
            cb_matrix=cb_matrix,
            clustering_model=clustering_model,
            interactions_df=interactions_df,
            items_df=cb_items_df,
            user_feats_df=user_feats_df
        )
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": f"Hybrid Recommendation error: {str(e)}"}), 500
