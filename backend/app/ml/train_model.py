import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import os

# === CONFIGURATION ===
DATA_PATH = 'Cleaned_Travel_Dataset_ModelReady.csv.gz'
TARGET_COLUMN = 'booking_price'  # <- Change if you're predicting a different value
MODEL_OUTPUT = 'trained_rf_model.pkl'

# === STEP 1: Load Dataset ===
print("📥 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# === STEP 2: Drop non-numeric or irrelevant columns (like dates or IDs) ===
drop_cols = ['Trip ID', 'Traveler name', 'Start date', 'End date', 'Website', 'Address']
df = df.drop(columns=[col for col in drop_cols if col in df.columns])

# === STEP 3: Handle missing values (if any remain) ===
df = df.dropna()

# === STEP 4: Split into features & target ===
X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

# Optional: Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === STEP 5: Train-test split ===
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
print(f"🧪 Training size: {X_train.shape}, Testing size: {X_test.shape}")

# === STEP 6: Train model ===
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("✅ Model training complete.")

# === STEP 7: Evaluate model ===
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"📊 Evaluation:")
print(f" - Mean Squared Error: {mse:.4f}")
print(f" - R² Score: {r2:.4f}")

# === STEP 8: Save model & scaler ===
joblib.dump(model, MODEL_OUTPUT)
joblib.dump(scaler, 'scaler.pkl')
print(f"💾 Model saved to: {MODEL_OUTPUT}")
