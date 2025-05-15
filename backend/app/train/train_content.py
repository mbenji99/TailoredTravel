import pandas as pd
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# === Configuration ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_ratings_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "content_model.pkl")

# === Step 1: Load and Clean Dataset ===
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Clean price column
def clean_price(val):
    try:
        return float(str(val).replace('$', '').replace('USD', '').replace(',', '').strip())
    except:
        return 0.0

df['price'] = df['price'].apply(clean_price)

# Fill missing values and combine key features
df['destination'] = df['destination'].fillna('')
df['accommodation_type'] = df['accommodation_type'].fillna('')
df['content'] = df[['destination', 'accommodation_type']].astype(str).agg(' '.join, axis=1)

# === Step 2: Generate TF-IDF Matrix ===
print("Training TF-IDF vectorizer...")
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['content'])

# === Step 3: Compute Cosine Similarities ===
print("Computing cosine similarity matrix...")
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# === Step 4: Save Model and Data ===
os.makedirs(MODEL_DIR, exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump((cosine_sim, df), f)

print(f"Content-based model saved to: {MODEL_PATH}")

# === Step 5: Recommendation Function ===
def get_recommendations(item_index: int, top_n: int = 5):
    if item_index < 0 or item_index >= len(df):
        raise ValueError("Invalid item index provided.")
    
    sim_scores = list(enumerate(cosine_sim[item_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]

    return [
        {
            "destination": df.iloc[i]["destination"],
            "accommodation_type": df.iloc[i]["accommodation_type"],
            "price": df.iloc[i]["price"],
            "similarity_score": round(score, 4)
        }
        for i, score in sim_scores
    ]

# === Optional CLI for Testing ===
if __name__ == "__main__":
    try:
        print("\nAvailable items:")
        for idx, row in df.iterrows():
            print(f"{idx}: {row['destination']} - {row['accommodation_type']}")

        index = int(input("\nEnter item index for recommendations: "))
        results = get_recommendations(index)

        print("\nTop Recommendations:")
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['destination']} ({item['accommodation_type']}), "
                  f"Price: ${item['price']}, Similarity: {item['similarity_score']}")

    except ValueError as e:
        print(f"Error: {e}")
