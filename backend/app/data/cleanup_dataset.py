import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Load dataset
df = pd.read_csv("cleaned_feature_hybrid_dataset.csv")

# Step 1: Normalize 'interaction' to a 1-5 rating scale using Min-Max
scaler = MinMaxScaler(feature_range=(1, 5))
df['rating'] = scaler.fit_transform(df[['interaction']])
df['rating'] = df['rating'].round(2)  # Round to 2 decimal places

# Step 2: Drop exact duplicates (optional but useful)
df = df.drop_duplicates()

# Step 3: Encode categorical features
label_encoders = {}
for col in ['user_id', 'item_id', 'destination', 'accommodation_type', 'gender', 'nationality']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Step 4: Final dataset structure
clean_df = df[[
    'user_id',
    'item_id',
    'rating',  # This is your target for recommender system
    'destination',
    'accommodation_type',
    'price',
    'age',
    'gender',
    'nationality'
]]

# Save cleaned data
clean_df.to_csv("cleaned_ratings_data.csv", index=False)
print("Cleaned data saved to 'cleaned_ratings_data.csv'")
