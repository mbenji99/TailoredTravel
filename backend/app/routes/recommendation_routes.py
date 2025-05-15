from flask import Blueprint, request, jsonify
from app.core.hybrid_recommender import recommend_items
from services.ratings_service import store_rating
from services.history_service import save_recommendation_history, get_recommendation_history

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendations/hybrid', methods=['POST'])
def get_hybrid_recommendations():
    try:
        data = request.get_json()
        print("🔍 Incoming data:", data)

        required_fields = ['user_id', 'budget']
        missing_fields = [field for field in required_fields if data.get(field) is None]
        if missing_fields:
            return jsonify({'error': f"Missing required fields: {', '.join(missing_fields)}"}), 400

        user_id = data['user_id']
        budget = data['budget']
        weather = data.get('weather')
        destination = data.get('destination')
        activities = data.get('activities')
        accommodation_type = data.get('accommodation_type')
        top_n = data.get('top_n', 3)

        print(
            f"📊 Filtering with: user_id={user_id}, budget={budget}, weather={weather}, "
            f"destination={destination}, activities={activities}, accommodation_type={accommodation_type}, top_n={top_n}"
        )

        recommendations = recommend_items(
            user_id=user_id,
            budget=budget,
            weather=weather,
            destination=destination,
            activities=activities,
            accommodation_type=accommodation_type,
            top_n=top_n
        )

        if isinstance(recommendations, list) and recommendations:
            save_recommendation_history(user_id, recommendations)

        return jsonify({'recommendations': recommendations}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f"Failed to get hybrid recommendations: {str(e)}"}), 500


@recommendation_bp.route('/rate', methods=['POST'])
def rate_item():
    try:
        data = request.get_json()
        required_fields = ['user_id', 'item_id', 'rating']
        missing = [f for f in required_fields if data.get(f) is None]
        if missing:
            return jsonify({'error': f"Missing required fields: {', '.join(missing)}"}), 400

        store_rating(data['user_id'], data['item_id'], data['rating'])
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
