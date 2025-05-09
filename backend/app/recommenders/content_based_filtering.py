from sklearn.metrics.pairwise import linear_kernel

def get_cb_recommendations(hotel_id, num_recommendations, model_data):
    """Recommend hotels based on content similarity to a given hotel ID."""
    tfidf_matrix = model_data['tfidf_matrix']
    hotels_df = model_data['hotels_df']

    if hotel_id not in hotels_df['id'].values:
        raise ValueError(f"Hotel ID {hotel_id} not found in dataset.")

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    idx = hotels_df.index[hotels_df['id'] == hotel_id][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sim_scores[1:num_recommendations + 1]]
    return hotels_df.iloc[top_indices].to_dict(orient='records')
