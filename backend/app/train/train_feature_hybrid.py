import pandas as pd
import os

# Set up proper data path
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")

# Load data
items_df = pd.read_csv(os.path.join(DATA_DIR, "cleaned_items.csv"))
interactions_df = pd.read_csv(os.path.join(DATA_DIR, "cleaned_interactions.csv"))
users_df = pd.read_csv(os.path.join(DATA_DIR, "user_features.csv"))

# Show loaded columns
print("Items columns:", list(items_df.columns))
print("Interactions columns:", list(interactions_df.columns))
print("User features columns:", list(users_df.columns))

# Merge interactions with items
merged_df = interactions_df.merge(items_df, on='item_id', how='left')

# Merge with user features
merged_df = merged_df.merge(users_df, on='user_id', how='left')

# Show preview of the merged dataframe
print("\nPreview of merged feature set:")
print(merged_df.head())

# Save to file for model training
output_path = os.path.join(DATA_DIR, "feature_hybrid_dataset.csv")
merged_df.to_csv(output_path, index=False)
print(f"\nFeature hybrid dataset saved to {output_path}")
