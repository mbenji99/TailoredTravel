import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def train_content(items_df):
    # Create a synthetic description from destination, accommodation_type, and price
    items_df['description'] = (
        items_df['destination'].astype(str) + " " +
        items_df['accommodation_type'].astype(str) + " " +
        items_df['price'].astype(str)
    )

    # Fill missing descriptions if any
    items_df['description'] = items_df['description'].fillna('')

    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(items_df['description'])

    return tfidf, tfidf_matrix

def compute_similarity_matrix(tfidf_matrix):
    # Compute cosine similarity matrix
    return linear_kernel(tfidf_matrix, tfidf_matrix)

def save_cb_model(tfidf, similarity_matrix, items_df, filename="app/models/content_model.pkl"):
    # Save TF-IDF model, similarity matrix, and item index mapping
    with open(filename, "wb") as f:
        pickle.dump({
            "tfidf": tfidf,
            "similarity_matrix": similarity_matrix,
            "item_ids": list(items_df["item_id"])
        }, f)
    print(f"Model saved to {filename}")

def main():
    print("Loading hotel data...")
    
    # Use the correct absolute path for your CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'cleaned_items.csv')
    
    # Check if the file exists at the resolved path
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return
    
    hotels_df = pd.read_csv(csv_path)

    print("Training content-based model...")
    tfidf, tfidf_matrix = train_content(hotels_df)
    similarity_matrix = compute_similarity_matrix(tfidf_matrix)

    print("Saving model...")
    save_cb_model(tfidf, similarity_matrix, hotels_df)
    print("Done.")

if __name__ == "__main__":
    main()
