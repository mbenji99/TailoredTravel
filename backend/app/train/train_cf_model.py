import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dot
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import save_model


# Load interactions
interactions = pd.read_csv('../data/cleaned_interactions.csv')

# Encode user and item IDs
user_ids = interactions['user_id'].astype("category").cat.codes.values
item_ids = interactions['item_id'].astype("category").cat.codes.values
ratings = interactions['rating'].values if 'rating' in interactions else np.ones(len(interactions))

num_users = len(set(user_ids))
num_items = len(set(item_ids))

# Build simple matrix factorization model
user_input = Input(shape=(1,))
item_input = Input(shape=(1,))
user_vec = Embedding(num_users, 50)(user_input)
item_vec = Embedding(num_items, 50)(item_input)
user_vec = Flatten()(user_vec)
item_vec = Flatten()(item_vec)
dot = Dot(axes=1)([user_vec, item_vec])

model = Model(inputs=[user_input, item_input], outputs=dot)
model.compile(optimizer=Adam(0.001), loss='mse')

# Train model
model.fit([user_ids, item_ids], ratings, epochs=5, batch_size=64, verbose=1)

# Save model
os.makedirs('../models', exist_ok=True)
model.save('../models/cf_model.h5')
print("✅ CF model trained and saved.")