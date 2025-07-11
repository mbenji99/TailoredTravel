import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import joblib
import os

# === CONFIGURATION ===
NUM_CLUSTERS = 5
CLUSTER_MODEL_PATH = "../models/clustering_model.pkl"
PREPROCESSOR_PATH = "../models/user_preprocessor.pkl"
DATASET_PATH = "../data/feature_hybrid_dataset.csv"

# Ensure the models directory exists
os.makedirs(os.path.dirname(CLUSTER_MODEL_PATH), exist_ok=True)

def preprocess_user_features(df: pd.DataFrame) -> tuple:
    """Extract and preprocess user features for clustering, with imputation."""
    print("[INFO] Preprocessing user features...")
    user_features = df[['user_id', 'age', 'gender', 'nationality']].drop_duplicates()

    # Define preprocessors with imputation
    numeric_pipeline = Pipeline([ 
        ("imputer", SimpleImputer(strategy='mean')),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([ 
        ("imputer", SimpleImputer(strategy='most_frequent')),
        ("encoder", OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([ 
        ("num", numeric_pipeline, ['age']),
        ("cat", categorical_pipeline, ['gender', 'nationality'])
    ])

    # Fit and transform
    processed = preprocessor.fit_transform(user_features)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    print(f"[INFO] Preprocessor saved at {PREPROCESSOR_PATH}")

    return processed, user_features

def cluster_users(df: pd.DataFrame) -> pd.DataFrame:
    """Assign users to clusters based on demographic features."""
    print("[INFO] Clustering users...")
    X_processed, user_features = preprocess_user_features(df)

    kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42)
    user_features['cluster'] = kmeans.fit_predict(X_processed)

    joblib.dump(kmeans, CLUSTER_MODEL_PATH)
    print(f"[INFO] Clustering model saved at {CLUSTER_MODEL_PATH}")

    return user_features[['user_id', 'cluster']]

def get_top_items_per_cluster(df: pd.DataFrame, item_data: pd.DataFrame, cluster_col='cluster', top_n=3) -> pd.DataFrame:
    """Return top N popular items for each cluster."""
    # Merge the user cluster information with the interaction data
    merged_df = df.merge(item_data[['user_id', 'item_id']], on='user_id', how='left')
    
    top_items = (
        merged_df.groupby([cluster_col, 'item_id'])
        .size()
        .reset_index(name='count')
        .sort_values(['cluster', 'count'], ascending=[True, False])
    )

    return top_items.groupby('cluster').head(top_n)

def get_cluster_recommendations(user_id: str, df: pd.DataFrame, top_items_by_cluster: pd.DataFrame) -> list:
    """Recommend top items from user's cluster."""
    if user_id in df['user_id'].values:
        cluster = df[df['user_id'] == user_id]['cluster'].iloc[0]
        recommendations = top_items_by_cluster[top_items_by_cluster['cluster'] == cluster]
        return recommendations['item_id'].tolist()
    else:
        print(f"[INFO] User {user_id} not found in the dataset.")
        return []

if __name__ == "__main__":
    print("[INFO] Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    print(f"[INFO] Dataset loaded with shape {df.shape}")
    
    # Cluster the users based on demographic features
    clustered_df = cluster_users(df)
    print("[INFO] Clustering complete.")

    # Load item interaction data
    item_data = df[['user_id', 'item_id']]  # Or load another file containing item interactions
    print(f"[INFO] Item data loaded with shape {item_data.shape}")

    # Get the top items per cluster
    top_items_by_cluster = get_top_items_per_cluster(clustered_df, item_data)
    print(f"[INFO] Top items by cluster:\n{top_items_by_cluster}")

    # Example of generating recommendations for a specific user
    user_id = "John Smith"  # Replace with an actual user ID
    recommendations = get_cluster_recommendations(user_id, clustered_df, top_items_by_cluster)
    print(f"[INFO] Recommendations for {user_id}: {recommendations}")
