import pandas as pd
import os
import pickle
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy

# ---------- CONFIG ----------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_ratings_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "svd_model.pkl")

# ---------- STEP 1: Load Preprocessed Ratings Data ----------

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Check required columns
required_cols = {"user_id", "item_id", "rating"}
if not required_cols.issubset(df.columns):
    raise ValueError(f"❌ Missing required columns. Found columns: {list(df.columns)}")

# Optional: Clip ratings to ensure within 1–5 range
df["rating"] = df["rating"].clip(lower=1.0, upper=5.0)

# ---------- STEP 2: Prepare Data for Surprise ----------

print("Preparing data for training...")
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[["user_id", "item_id", "rating"]], reader)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# ---------- STEP 3: Train SVD Collaborative Filtering Model ----------

print("Training SVD collaborative filtering model...")
model = SVD()
model.fit(trainset)

# ---------- STEP 4: Evaluate Model ----------

print("Evaluating model...")
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"Test RMSE: {rmse:.4f}")

# ---------- STEP 5: Save Trained Model ----------

print("Saving model...")
os.makedirs(MODEL_DIR, exist_ok=True)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("Collaborative Filtering model trained and saved successfully at:")
print(f"   {MODEL_PATH}")
