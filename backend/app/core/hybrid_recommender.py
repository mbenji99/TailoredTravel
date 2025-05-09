import numpy as np
from typing import Dict, List
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

class HybridRecommender:
    def __init__(self, cf_model, content_model, clustering_model, weights=None):
        """
        Initialize hybrid recommender with component models.
        
        Args:
            cf_model: Collaborative filtering model (e.g., SVD from surprise library)
            content_model: Content-based filtering model (e.g., TF-IDF for descriptions)
            clustering_model: Clustering model (e.g., KMeans for clustering users/items)
            weights: Dictionary with weights for each model (default: {'cf': 0.4, 'content': 0.4, 'cluster': 0.2})
        """
        self.cf_model = cf_model
        self.content_model = content_model
        self.clustering_model = clustering_model
        self.weights = weights or {'cf': 0.4, 'content': 0.4, 'cluster': 0.2}
        self.scaler = MinMaxScaler()
        
    def recommend(self, user_id: int, item_ids: List[int], n_recommendations: int = 10) -> Dict:
        """
        Generate hybrid recommendations for a user.
        
        Args:
            user_id: ID of the user
            item_ids: List of candidate item IDs
            n_recommendations: Number of recommendations to return
            
        Returns:
            Dictionary with recommendations and scores
        """
        try:
            # Get predictions from each model
            cf_scores = self._get_cf_scores(user_id, item_ids)
            content_scores = self._get_content_scores(user_id, item_ids)
            cluster_scores = self._get_cluster_scores(user_id, item_ids)
            
            # Normalize scores
            all_scores = np.array([cf_scores, content_scores, cluster_scores])
            normalized_scores = self.scaler.fit_transform(all_scores.T).T
            
            # Apply weights and combine
            weighted_scores = (
                normalized_scores[0] * self.weights['cf'] +
                normalized_scores[1] * self.weights['content'] +
                normalized_scores[2] * self.weights['cluster']
            )
            
            # Get top recommendations
            top_indices = np.argsort(weighted_scores)[-n_recommendations:][::-1]
            recommendations = {
                'items': [item_ids[i] for i in top_indices],
                'scores': [float(weighted_scores[i]) for i in top_indices]
            }
            
            return recommendations
            
        except Exception as e:
            raise ValueError(f"Error generating recommendations: {str(e)}")
    
    def _get_cf_scores(self, user_id, item_ids):
        """
        Calculate collaborative filtering scores for the user on the given items.
        
        Args:
            user_id: The ID of the user
            item_ids: List of item IDs to recommend
            
        Returns:
            List of collaborative filtering scores for the items
        """
        cf_scores = []
        for item_id in item_ids:
            # Use the collaborative filtering model (e.g., SVD) to predict rating for the user-item pair
            pred_rating = self.cf_model.predict(user_id, item_id).est  # For example using `surprise` SVD
            cf_scores.append(pred_rating)
        return np.array(cf_scores)
    
    def _get_content_scores(self, user_id, item_ids):
        """
        Calculate content-based scores for the user on the given items.
        
        Args:
            user_id: The ID of the user
            item_ids: List of item IDs to recommend
            
        Returns:
            List of content-based scores for the items based on their descriptions
        """
        content_scores = []
        for item_id in item_ids:
            # Get the content-based score (e.g., similarity between item and user’s preferences)
            # Assuming content_model has a method `predict` or some form of similarity computation
            content_score = self.content_model.predict(user_id, item_id)
            content_scores.append(content_score)
        return np.array(content_scores)
    
    def _get_cluster_scores(self, user_id, item_ids):
        """
        Calculate clustering scores for the user on the given items.
        
        Args:
            user_id: The ID of the user
            item_ids: List of item IDs to recommend
            
        Returns:
            List of clustering scores based on the user's cluster and item similarity
        """
        # Predict the user's cluster (you may use a clustering model like KMeans)
        user_cluster = self.clustering_model.predict([user_id])[0]  # Assuming the model is KMeans or similar
        cluster_scores = []
        
        for item_id in item_ids:
            # Calculate similarity to the user's cluster or cluster-based score
            # Assuming `get_item_cluster_similarity` calculates the item's cluster-based score
            cluster_score = self.clustering_model.get_item_cluster_similarity(user_cluster, item_id)
            cluster_scores.append(cluster_score)
        
        return np.array(cluster_scores)
def get_hybrid_recommendations(user_id, num_recommendations, cf_model, cb_model, clustering_model,
                                interactions_df, items_df, user_feats_df):
    """
    Helper function to create and use HybridRecommender to generate recommendations.
    
    Args:
        user_id: ID of the user
        num_recommendations: How many recommendations to return
        cf_model: Collaborative filtering model
        cb_model: Content-based model
        clustering_model: Clustering model
        interactions_df: DataFrame with user-item interactions
        items_df: DataFrame with item metadata
        user_feats_df: DataFrame with user features

    Returns:
        Dictionary with recommended item IDs and scores
    """
    # Get list of candidate item IDs (those not interacted with by the user)
    user_history = interactions_df[interactions_df['user_id'] == user_id]['item_id'].unique()
    candidate_items = items_df[~items_df['item_id'].isin(user_history)]['item_id'].tolist()

    # Instantiate HybridRecommender and get recommendations
    recommender = HybridRecommender(cf_model, cb_model, clustering_model)
    return recommender.recommend(user_id, candidate_items, n_recommendations=num_recommendations)

