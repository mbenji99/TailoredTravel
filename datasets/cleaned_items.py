import pandas as pd
import os

# Set up proper data path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "backend", "app", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Load and clean
df = pd.read_csv("Travel details dataset.csv")

items = df[['Destination', 'Accommodation type', 'Accommodation cost']].drop_duplicates().rename(columns={
    'Destination': 'destination',
    'Accommodation type': 'accommodation_type',
    'Accommodation cost': 'price'
})

# Add item_id
items['item_id'] = items.apply(lambda row: f"{row['destination']}_{row['accommodation_type']}", axis=1)
items = items[['item_id', 'destination', 'accommodation_type', 'price']]

# Save
items.to_csv(os.path.join(DATA_DIR, "cleaned_items.csv"), index=False)
print("✅ cleaned_items.csv created with item_id.")
