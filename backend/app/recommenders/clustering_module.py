from sklearn.cluster import KMeans
import pandas as pd

def perform_clustering(df, n_clusters=3):
    features = df[['price']]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(features)
    return df, kmeans

def get_cluster_recommendations(df, user_id):
    df, model = perform_clustering(df)
    user_cluster = df[df['user_id'] == user_id]['cluster'].iloc[0]
    return df[df['cluster'] == user_cluster].head(5)
