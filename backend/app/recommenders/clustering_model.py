# === File: app/recommenders/clustering_model.py ===

import os
import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# === Paths ===
MODEL_PATH = 'app/models/clustering_model.pkl'
PREPROCESSOR_PATH = 'app/models/user_preprocessor.pkl'


def train_clustering(user_features_df, n_clusters=5, model_path=MODEL_PATH, preprocessor_path=PREPROCESSOR_PATH):
    try:
        if user_features_df.empty:
            raise ValueError("Input DataFrame is empty.")

        # Extract and preprocess features
        features = user_features_df[['user_id', 'age', 'gender', 'nationality']].drop_duplicates()
        preprocessor = ColumnTransformer([
            ("num", StandardScaler(), ['age']),
            ("cat", OneHotEncoder(), ['gender', 'nationality'])
        ])
        X_processed = preprocessor.fit_transform(features)

        # Train model
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        features['cluster'] = kmeans.fit_predict(X_processed)

        # Save model and preprocessor
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(kmeans, model_path)
        joblib.dump(preprocessor, preprocessor_path)

        return kmeans, features

    except Exception as e:
        raise Exception(f"Error training clustering model: {str(e)}")


def load_clustering_model(path: str):
    full_path = os.path.join(os.path.dirname(__file__), '..', path)
    full_path = os.path.abspath(full_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Clustering model not found at {full_path}")
    
    return joblib.load(full_path)

def load_preprocessor(path=PREPROCESSOR_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Preprocessor not found at {path}")
    return joblib.load(path)


def get_user_cluster_recommendations(user_id, num_recommendations, model, user_feats_df, interactions_df):
    if user_id not in user_feats_df['user_id'].values:
        raise ValueError(f"User ID {user_id} not found in user feature data.")

    # Preprocess using saved pipeline
    preprocessor = load_preprocessor()
    user_features = user_feats_df[['user_id', 'age', 'gender', 'nationality']].drop_duplicates()
    X_processed = preprocessor.transform(user_features)

    # Predict cluster for all users
    user_features['cluster'] = model.predict(X_processed)

    # Get user cluster
    user_cluster = user_features[user_features['user_id'] == user_id]['cluster'].values[0]
    cluster_user_ids = user_features[user_features['cluster'] == user_cluster]['user_id'].tolist()

    # Filter interactions by users in same cluster
    cluster_interactions = interactions_df[interactions_df['user_id'].isin(cluster_user_ids)]

    # Recommend most interacted items in the cluster
    top_items = (
        cluster_interactions.groupby('item_id')
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(num_recommendations)
    )

    return top_items['item_id'].tolist()
