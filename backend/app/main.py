from flask import Flask
from flask_cors import CORS
import sys
import os
import mysql.connector
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Ensure backend module visibility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Blueprint imports
from app.api.recommendations import recommendations_bp
from app.routes.recommendation_routes import recommendation_bp
from app.routes.history_routes import history_bp  

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(recommendations_bp, url_prefix="/api/recommendations")
app.register_blueprint(recommendation_bp, url_prefix="/api")
app.register_blueprint(history_bp, url_prefix="/api")

@app.route("/", methods=["GET"])
def home():
    return {"message": "Travel Recommender Backend is running 🚀"}

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
        if connection.is_connected():
            print("✅ Successfully connected to the MySQL database.")
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None

if __name__ == "__main__":
    connect_to_db()  
    app.run(debug=True)
