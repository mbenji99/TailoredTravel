import pandas as pd
import os

# Set up proper data path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "backend", "app", "data")
os.makedirs(DATA_DIR, exist_ok=True)

df = pd.read_csv("Travel details dataset.csv")

interactions = df[[
    'Traveler name',
    'Destination',
    'Accommodation type',
    'Accommodation cost',
    'Transportation cost'
]].copy()

# Create item_id and rename user_id
interactions['item_id'] = interactions.apply(lambda row: f"{row['Destination']}_{row['Accommodation type']}", axis=1)
interactions['user_id'] = interactions['Traveler name']

# Calculate interaction value (total cost)
interactions['interaction'] = interactions['Accommodation cost'] + interactions['Transportation cost']

# Select relevant columns
interactions = interactions[['user_id', 'item_id', 'interaction']]

# Save
interactions.to_csv(os.path.join(DATA_DIR, "cleaned_interactions.csv"), index=False)
print("✅ cleaned_interactions.csv created.")
