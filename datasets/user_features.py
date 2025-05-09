import pandas as pd
import os

# Set up proper data path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "backend", "app", "data")
os.makedirs(DATA_DIR, exist_ok=True)

df = pd.read_csv("Travel details dataset.csv")

users = df[[
    'Traveler name',
    'Traveler age',
    'Traveler gender',
    'Traveler nationality'
]].drop_duplicates().rename(columns={
    'Traveler name': 'user_id',
    'Traveler age': 'age',
    'Traveler gender': 'gender',
    'Traveler nationality': 'nationality'
})

users.to_csv(os.path.join(DATA_DIR, "user_features.csv"), index=False)
print("✅ user_features.csv created.")
