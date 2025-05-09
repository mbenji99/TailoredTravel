import pandas as pd

INTERACTIONS_FILE = "app/data/cleaned_interactions.csv"

def store_rating(user_id, item_id, rating):
    df = pd.read_csv(INTERACTIONS_FILE)

    new_entry = pd.DataFrame([{
        "user_id": user_id,
        "item_id": item_id,
        "interaction": rating
    }])

    updated_df = pd.concat([df, new_entry], ignore_index=True)
    updated_df.to_csv(INTERACTIONS_FILE, index=False)
