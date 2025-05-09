import os
import json
from datetime import datetime

# Get absolute base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
HISTORY_FILE = os.path.join(DATA_DIR, "user_recommendation_history.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Ensure history file exists and is initialized
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def save_recommendation_history(user_id, recommendations):
    # Load existing history
    with open(HISTORY_FILE, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []

    # Add new entries
    new_entries = []
    for rec in recommendations:
        new_entries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "item_id": rec.get("item_id"),
            "destination_name": rec.get("destination_name", ""),
            "predicted_rating": rec.get("predicted_rating", None)
        })

    history.extend(new_entries)

    # Save updated history
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_recommendation_history(user_id=None):
    with open(HISTORY_FILE, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []

    if user_id:
        return [entry for entry in history if entry["user_id"] == user_id]
    return history
import os
import json
from datetime import datetime

# Get absolute base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
HISTORY_FILE = os.path.join(DATA_DIR, "user_recommendation_history.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Ensure history file exists and is initialized
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def save_recommendation_history(user_id, recommendations):
    # Load existing history
    with open(HISTORY_FILE, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []

    # Add new entries
    new_entries = []
    for rec in recommendations:
        new_entries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "item_id": rec.get("item_id"),
            "destination_name": rec.get("destination_name", ""),
            "predicted_rating": rec.get("predicted_rating", None)
        })

    history.extend(new_entries)

    # Save updated history
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_recommendation_history(user_id=None):
    with open(HISTORY_FILE, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []

    if user_id:
        return [entry for entry in history if entry["user_id"] == user_id]
    return history
