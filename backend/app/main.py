from flask import Flask
from flask_cors import CORS
import sys
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Ensure backend module visibility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Blueprint imports
from app.routes.auth_routes import auth_bp
from app.api.recommendations import recommendations_bp  # Import the updated recommendations blueprint
from app.routes.recommendation_routes import recommendation_bp  # Ensure this is correctly imported
from app.routes.history_routes import history_bp  

# DB connection
from app.utils.db import connect_to_db

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS (including preflight OPTIONS) for your React origin
CORS(
    app,
    origins=["http://localhost:5173"],  # Front-end origin URL
    methods=["GET", "POST", "OPTIONS"],
    supports_credentials=True
)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(recommendations_bp, url_prefix="/api/recommendations")  # Ensure recommendation routes are registered
app.register_blueprint(recommendation_bp, url_prefix="/api")  # This includes your `/recommendations` API route
app.register_blueprint(history_bp, url_prefix="/api")

@app.route("/", methods=["GET"])
def home():
    return {"message": "Travel Recommender Backend is running 🚀"}

if __name__ == "__main__":
    try:
        connect_to_db()  
        print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

    app.run(debug=True, host="127.0.0.1", port=5000)  