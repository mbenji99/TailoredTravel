import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
import os
import sys

# === Step 1: Resolve paths correctly ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))                 # backend/app/train
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))     # backend/app/data
file_path = os.path.join(DATA_DIR, 'cleaned_items.csv')              # cleaned_items.csv

# === Step 2: Load and clean the items dataset ===
items_df = pd.read_csv(file_path)

# Normalize price column (strip currency symbols, commas, 'USD', etc.)
def clean_price(price):
    if pd.isna(price):
        return 0
    if isinstance(price, str):
        price = price.replace('$', '').replace('USD', '').replace(',', '').strip()
        try:
            return float(price)
        except:
            return 0
    return price

items_df['price'] = items_df['price'].apply(clean_price)

# Fill NaN and create 'content' column
items_df['destination'] = items_df['destination'].fillna('')
items_df['accommodation_type'] = items_df['accommodation_type'].fillna('')
items_df['content'] = items_df[['destination', 'accommodation_type']].astype(str).agg(' '.join, axis=1)

# === Step 3: Train TF-IDF model ===
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(items_df['content'])

# === Step 4: Compute cosine similarity ===
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# === Step 5: Save the trained model ===
MODEL_DIR = os.path.join('..', 'models')  
os.makedirs(MODEL_DIR, exist_ok=True)    

output_path = os.path.join(MODEL_DIR, 'content_model.pkl')
with open(output_path, 'wb') as f:
    pickle.dump((cosine_sim, items_df), f)

print("✅ Content-based model saved.")

# === Step 6: Recommendation Function ===
def get_recommendations(item_index, top_n=5):
    if item_index < 0 or item_index >= len(items_df):
        print("Invalid item index.")
        return []

    sim_scores = list(enumerate(cosine_sim[item_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    recommended_items = []
    for i, score in sim_scores:
        recommended_items.append({
            "destination": items_df.iloc[i]["destination"],
            "accommodation_type": items_df.iloc[i]["accommodation_type"],
            "price": items_df.iloc[i]["price"],
            "similarity_score": round(score, 4)
        })

    return recommended_items

# === Step 7: Optional test (only in interactive mode) ===
if __name__ == "__main__":
    if sys.stdin.isatty():
        print("\nAvailable items:")
        for idx, row in items_df.iterrows():
            print(f"{idx}: {row['destination']} - {row['accommodation_type']}")

        try:
            index = int(input("\nEnter item index for recommendations: "))
            top_recommendations = get_recommendations(index)

            print("\nTop Recommendations:")
            for i, rec in enumerate(top_recommendations, 1):
                print(f"{i}. {rec['destination']} ({rec['accommodation_type']}), Price: ${rec['price']}, Similarity: {rec['similarity_score']}")
        except ValueError:
            print("Please enter a valid integer index.")
