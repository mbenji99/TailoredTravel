import pandas as pd
import re
import pickle
import os
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy


# ---------- STEP 1: Load and Clean Data ----------

def extract_numeric_rating(val):
    if pd.isna(val):
        return None

    val = str(val).replace(",", "").replace("USD", "").replace("$", "").strip()
    numbers = [int(n) for n in re.findall(r'\d+', val)]

    if not numbers:
        return None
    elif len(numbers) == 1:
        return numbers[0]
    else:
        return sum(numbers) / len(numbers)

# Load and preprocess interaction data
interactions_df = pd.read_csv("app/data/cleaned_interactions.csv")
interactions_df = interactions_df.rename(columns={"interaction": "rating"})
interactions_df["rating"] = interactions_df["rating"].apply(extract_numeric_rating)
interactions_df = interactions_df.dropna(subset=["rating"])

# Normalize ratings to 1-5 scale
min_rating = interactions_df["rating"].min()
max_rating = interactions_df["rating"].max()

interactions_df["rating"] = interactions_df["rating"].apply(
    lambda x: 1 + 4 * ((x - min_rating) / (max_rating - min_rating))
)

# ---------- STEP 2: Train SVD Model ----------

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(interactions_df[["user_id", "item_id", "rating"]], reader)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

model = SVD()
model.fit(trainset)

# ---------- STEP 3: Evaluate Model ----------

predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"Test RMSE: {rmse:.4f}")

# ---------- STEP 4: Save Model ----------

# Ensure the models directory exists
os.makedirs("backend/app/models", exist_ok=True)

with open("app/models/svd_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully.")
