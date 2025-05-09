import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# === PATH TO DATA ===
CSV_PATH = r'C:\Users\Suzette Benjamin\Documents\Group Project\TailoredTravel\backend\app\data\cleaned_feature_hybrid_dataset.csv'

# === LOAD DATA ===
df = pd.read_csv(CSV_PATH)

# === CLUSTERING LOGIC ===
def perform_clustering(data, n_clusters=5):
    clustering_features = ['price', 'age']  # Can expand if needed
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data[clustering_features])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled)
    data['cluster'] = clusters
    return data, kmeans, scaler

def get_user_cluster_recommendations(user_id, df_clustered):
    user_data = df_clustered[df_clustered['user_id'] == user_id]
    if user_data.empty:
        return pd.DataFrame()
    user_cluster = user_data.iloc[0]['cluster']
    cluster_recs = df_clustered[(df_clustered['cluster'] == user_cluster) & (df_clustered['user_id'] != user_id)]
    return cluster_recs[['item_id', 'destination', 'accommodation_type', 'price']].drop_duplicates()

# === CONTENT-BASED FILTERING ===
def get_cb_recommendations(user_id, df):
    user_items = df[df['user_id'] == user_id]['item_id'].unique()
    item_features = df[['item_id', 'destination', 'accommodation_type']].drop_duplicates()

    # One-hot encode text features
    encoded = pd.get_dummies(item_features[['destination', 'accommodation_type']])
    encoded['item_id'] = item_features['item_id']
    encoded = encoded.set_index('item_id')

    # Mean feature vector for user's interacted items
    user_vector = encoded.loc[user_items].mean()

    # Cosine similarity to all items
    similarities = cosine_similarity([user_vector], encoded)[0]
    encoded['similarity'] = similarities

    top_items = encoded.sort_values('similarity', ascending=False).head(10)
    return df[df['item_id'].isin(top_items.index)][['item_id', 'destination', 'accommodation_type', 'price']].drop_duplicates()

# === COLLABORATIVE FILTERING ===
def get_cf_recommendations(user_id, df):
    interaction_matrix = df.pivot_table(index='user_id', columns='item_id', values='interaction').fillna(0)
    if user_id not in interaction_matrix.index:
        return pd.DataFrame()
    user_vector = interaction_matrix.loc[user_id].values.reshape(1, -1)
    similarity = cosine_similarity(user_vector, interaction_matrix.values)[0]
    similarity_series = pd.Series(similarity, index=interaction_matrix.index).drop(user_id)

    similar_users = similarity_series.sort_values(ascending=False).head(3).index
    recommended_items = interaction_matrix.loc[similar_users].mean().sort_values(ascending=False)
    recommended_items = recommended_items[recommended_items > 0].head(10).index

    return df[df['item_id'].isin(recommended_items)][['item_id', 'destination', 'accommodation_type', 'price']].drop_duplicates()

# === MAIN RECOMMENDER ===
def recommend_items(user_id, budget=3000.0):
    # Step 1: Cluster the data
    clustered_df, _, _ = perform_clustering(df.copy())

    # Step 2: Get recommendations
    cb_recs = get_cb_recommendations(user_id, df)
    cf_recs = get_cf_recommendations(user_id, df)
    cluster_recs = get_user_cluster_recommendations(user_id, clustered_df)

    # Step 3: Combine and filter unique recommendations
    all_recs = pd.concat([cb_recs, cf_recs, cluster_recs]).drop_duplicates('item_id')
    all_recs = all_recs.sort_values('price')
    all_recs = all_recs[all_recs['price'] <= budget]

    if all_recs.empty:
        print("No recommendations found within budget.")
        return

    # Step 4: Display top 3
    top3 = all_recs.head(3)
    print(f"Top 3 recommendations for '{user_id}' (Budget: ${budget:.2f}):")
    for idx, row in top3.iterrows():
        print(f"{row['destination']}_{row['accommodation_type']} — ${row['price']:.2f}")

    spent = top3['price'].sum()
    print(f"\n💰 Remaining budget: ${budget - spent:.2f}")

# === RUN EXAMPLE ===
if __name__ == "__main__":
    recommend_items('John Smith', budget=3000.0)
