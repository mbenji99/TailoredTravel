# backend/app/train/train_hybrid.py

import pandas as pd
import pickle
from surprise import Dataset, Reader, SVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os

# === Step 1: Load and clean interaction data ===
interactions_path = os.path.join("backend", "app", "data", "cleaned_interactions.csv")
items_path = os.path.join("app", "data", "cleaned_items.csv")

interactions_df = pd.read_csv(interactions_path)
items_df = pd.read_csv(items_path)

# Extract numeric ratings from 'interaction' column
def extract_rating(val):
    if pd.isna(val): return 0
    if isinstance(val, str):
        val = val.replace('$', '').replace('USD', '').replace(',', '').strip()
        parts = [float(s) for s in val.split() if s.replace('.', '', 1).isdigit()]
        return sum(parts) / len(parts) if parts else 0
    return val

interactions_df["rating"] = interactions_df["interaction"].apply(extract_rating)

# === Step 2: Train collaborative filtering (SVD) ===
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(interactions_df[['user_id', 'item_id', 'rating']], reader)
trainset = data.build_full_trainset()
cf_model = SVD()
cf_model.fit(trainset)

# === Step 3: Prepare content-based data ===
def clean_price(val):
    if pd.isna(val): return 0
    if isinstance(val, str):
        val = val.replace('$', '').replace('USD', '').replace(',', '').strip()
        try:
            return float(val)
        except:
            return 0
    return val

items_df['price'] = items_df['price'].apply(clean_price)
items_df['destination'] = items_df['destination'].fillna('')
items_df['accommodation_type'] = items_df['accommodation_type'].fillna('')
items_df['content'] = items_df[['destination', 'accommodation_type']].astype(str).agg(' '.join, axis=1)

# === Step 4: Train TF-IDF content-based model ===
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(items_df['content'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# === Step 5: Package and save hybrid model ===
item_index = pd.Series(items_df.index, index=items_df['destination']).to_dict()

hybrid_model = {
    'cf_model': cf_model,
    'cosine_sim': cosine_sim,
    'item_index': item_index,
    'items_df': items_df
}

output_path = os.path.join("backend", "app", "models", "hybrid_model.pkl")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'wb') as f:
    pickle.dump(hybrid_model, f)

print("✅ Hybrid model trained and saved to:", output_path)
