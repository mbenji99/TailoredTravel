from flask import Blueprint, request, jsonify
from services.history_service import save_recommendation_history, get_recommendation_history

history_bp = Blueprint('history', __name__)

@history_bp.route('/history/save', methods=['POST'])
def save_history():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        recommendations = data.get("recommendations")

        if not user_id or not recommendations:
            return jsonify({"error": "user_id and recommendations are required"}), 400

        save_recommendation_history(user_id, recommendations)
        return jsonify({"message": "History saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_bp.route('/history', methods=['GET'])
def get_history():
    try:
        user_id = request.args.get("user_id", type=int)

        if user_id is None:
            return jsonify({"error": "user_id is required"}), 400

        history = get_recommendation_history(user_id)
        return jsonify(history), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
