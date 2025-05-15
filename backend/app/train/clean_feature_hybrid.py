import pandas as pd
import re
import os

# Absolute path to the data folder
folder_path = r'C:\Users\Suzette Benjamin\Documents\Group Project\TailoredTravel\backend\app\data'

# Ensure the folder exists
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Load dataset
df = pd.read_csv('app/data/feature_hybrid_dataset.csv')

# Function to extract the largest price from a string with potential ranges
def extract_largest_price(value):
    # Remove any non-numeric characters except for the space and hyphen
    cleaned_value = re.sub(r'[^\d.\s-]', '', str(value)).strip()
    
    # Check if there is a range 
    if '-' in cleaned_value:
        # Split the range and get the maximum value
        try:
            prices = cleaned_value.split('-')
            largest_price = max(float(price.strip()) for price in prices)
            return largest_price
        except ValueError:
            return None  # If there's an error in conversion, return None
    else:
        # For single price entries, return the value itself
        try:
            price = float(cleaned_value)
            return price
        except ValueError:
            return None  # If conversion fails, return None

# Apply the function to the price column to create a new 'price' column with the largest value
df['price'] = df['price'].apply(extract_largest_price)

# Drop rows where price couldn't be parsed properly
df = df.dropna(subset=['price'])

# Clean the 'interaction' column (remove non-numeric characters and convert to float)
def clean_interaction(value):
    if pd.isna(value):
        return 0.0
    if isinstance(value, str):
        # Remove anything non-numeric from the 'interaction' column (e.g., '$', ',')
        cleaned = re.sub(r'[^\d.]', '', value)
        return float(cleaned) if cleaned else 0.0
    return float(value)

df['interaction'] = df['interaction'].apply(clean_interaction)

# Drop duplicates
df.drop_duplicates(inplace=True)

# Save cleaned data to new CSV using absolute path
df.to_csv(os.path.join(folder_path, 'cleaned_feature_hybrid_dataset.csv'), index=False)

print("Cleaned dataset saved to '{}'.".format(os.path.join(folder_path, 'cleaned_feature_hybrid_dataset.csv')))
