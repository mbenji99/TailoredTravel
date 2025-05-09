import os
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.decomposition import TruncatedSVD
from recommenders.clustering_model import train_clustering

# Load cleaned dataset

data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_feature_hybrid_dataset.csv')
df = pd.read_csv(data_path)
print(df.head())

# -----------------------------
# Step 1: Encode categorical features
# -----------------------------
user_encoder = LabelEncoder()
item_encoder = LabelEncoder()
gender_encoder = LabelEncoder()
nationality_encoder = LabelEncoder()
destination_encoder = LabelEncoder()
accommodation_encoder = LabelEncoder()

df['user_idx'] = user_encoder.fit_transform(df['user_id'])
df['item_idx'] = item_encoder.fit_transform(df['item_id'])
df['gender_idx'] = gender_encoder.fit_transform(df['gender'])
df['nationality_idx'] = nationality_encoder.fit_transform(df['nationality'])
df['destination_idx'] = destination_encoder.fit_transform(df['destination'])
df['accommodation_idx'] = accommodation_encoder.fit_transform(df['accommodation_type'])

# -----------------------------
# Step 2: Create user-item interaction matrix
# -----------------------------
interaction_matrix = df.pivot_table(index='user_idx', columns='item_idx', values='interaction', fill_value=0)

# -----------------------------
# Step 3: Apply SVD for collaborative filtering
# -----------------------------
svd = TruncatedSVD(n_components=50, random_state=42)
user_factors = svd.fit_transform(interaction_matrix)
item_factors = svd.components_.T

# -----------------------------
# Step 4: Create item content features matrix
# -----------------------------
item_metadata = df.drop_duplicates(subset='item_idx')[['item_idx', 'destination_idx', 'accommodation_idx', 'price']]
scaler = MinMaxScaler()
item_metadata['price_scaled'] = scaler.fit_transform(item_metadata[['price']])
item_content_features = item_metadata[['destination_idx', 'accommodation_idx', 'price_scaled']].values

# -----------------------------
# Step 5: Combine collaborative and content-based features
# -----------------------------
hybrid_item_features = np.hstack([item_factors, item_content_features])

# -----------------------------
# Step 6: Apply Clustering
# -----------------------------
user_features = df[['user_id', 'age', 'price']]  # Add other numerical features as needed
_, df_with_clusters = train_clustering(user_features, features=['age', 'price'])

# -----------------------------
# Step 7: Save everything
# -----------------------------
model_data = {
    'user_encoder': user_encoder,
    'item_encoder': item_encoder,
    'gender_encoder': gender_encoder,
    'nationality_encoder': nationality_encoder,
    'destination_encoder': destination_encoder,
    'accommodation_encoder': accommodation_encoder,
    'user_factors': user_factors,
    'hybrid_item_features': hybrid_item_features,
    'scaler': scaler,
    'user_clusters': df_with_clusters[['user_id', 'cluster']]
}

with open('models/hybrid_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print("✅ Hybrid recommendation model trained and saved to ../models/hybrid_model.pkl")
