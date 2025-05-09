import pandas as pd

def get_cf_recommendations(df, user_id):
    # Placeholder logic – replace with actual CF
    user_interacted = df[df['user_id'] == user_id]['item_id'].tolist()
    return df[~df['item_id'].isin(user_interacted)].head(5)
