from flask import Blueprint, request, jsonify
from services.recommendation_service import recommend_items
from services.ratings_service import store_rating
from services.history_service import save_recommendation_history, get_recommendation_history

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        user_id = request.args.get('user_id', type=int)
        budget = request.args.get('budget', type=float)
        weather = request.args.get('weather')
        environment = request.args.get('environment')
        activities = request.args.get('activities')

        if not user_id or budget is None:
            return jsonify({'error': 'user_id and budget are required'}), 400

        recommendations = recommend_items(user_id, budget, weather, environment, activities)

        # Save recommendations to history if valid results
        if isinstance(recommendations, list) and recommendations:
            save_recommendation_history(user_id, recommendations)

        return jsonify(recommendations), 200

    except Exception as e:
        return jsonify({'error': f"Failed to get recommendations: {str(e)}"}), 500


@recommendation_bp.route('/rate', methods=['POST'])
def rate_item():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        rating = data.get('rating')

        if not all([user_id, item_id, rating]):
            return jsonify({'error': 'Missing required fields'}), 400

        store_rating(user_id, item_id, rating)
        return jsonify({'message': 'Rating saved successfully'}), 200

    except Exception as e:
        return jsonify({'error': f"Failed to save rating: {str(e)}"}), 500


@recommendation_bp.route('/history', methods=['GET'])
def get_history():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400

        history = get_recommendation_history(user_id)
        return jsonify(history), 200

    except Exception as e:
        return jsonify({'error': f"Failed to fetch history: {str(e)}"}), 500
