import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib
from pathlib import Path

def train_content(items_df):
    items_df.columns = items_df.columns.str.strip().str.replace('\r', '', regex=False).str.replace('\n', '', regex=False)
    print("Loaded columns:", items_df.columns.tolist())

    items_df['description'] = items_df['destination'] + ' ' + items_df['accommodation_type'] + ' ' + items_df['price'].astype(str)
    items_df['description'] = items_df['description'].fillna('')

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(items_df['description'])

    return tfidf, tfidf_matrix

def compute_similarity_matrix(tfidf_matrix):
    return linear_kernel(tfidf_matrix, tfidf_matrix)

def save_cb_model(model_data, model_path):
    joblib.dump(model_data, model_path)

def load_cb_model(model_path):
    return joblib.load(model_path)

if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent.parent / 'data' / 'cleaned_items.csv'
    items_df = pd.read_csv(data_path)
    print("Fixed columns:", items_df.columns.tolist())

    tfidf, tfidf_matrix = train_content(items_df)
    similarity_matrix = compute_similarity_matrix(tfidf_matrix)

    model_dict = {
        "tfidf_model": tfidf,
        "tfidf_matrix": tfidf_matrix,
        "similarity_matrix": similarity_matrix,
        "hotels_df": items_df
    }

    model_save_path = Path(__file__).resolve().parent.parent / 'models' / 'content_based_model.pkl'
    model_save_path.parent.mkdir(parents=True, exist_ok=True)
    save_cb_model(model_dict, model_save_path)

    model_data = load_cb_model(model_save_path)
