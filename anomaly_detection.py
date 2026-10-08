import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import joblib

# -----------------------------
# 1. Load dataset
# -----------------------------

df = pd.read_csv("data/campus_data.csv")

# -----------------------------
# 2. Convert equipment status
# -----------------------------

encoder = LabelEncoder()

df["equipment_status_encoded"] = encoder.fit_transform(
    df["equipment_status"]
)

# -----------------------------
# 3. Select AI features
# -----------------------------

features = [
    "occupancy",
    "class_scheduled",
    "temperature",
    "electricity_kwh",
    "water_liters",
    "equipment_status_encoded",
    "ac_status",
    "light_status",
    "fan_status"
]

X = df[features]

# -----------------------------
# 4. Create AI model
# -----------------------------

model = IsolationForest(
    n_estimators=200,
    contamination=0.025,
    random_state=42
)

# -----------------------------
# 5. Train model
# -----------------------------

model.fit(X)

# -----------------------------
# 6. Predict anomalies
# -----------------------------

df["ai_prediction"] = model.predict(X)

# Isolation Forest:
#  1  = normal
# -1  = anomaly

df["ai_anomaly"] = (
    df["ai_prediction"] == -1
).astype(int)

# -----------------------------
# 7. Save model
# -----------------------------

joblib.dump(
    model,
    "models/anomaly_model.pkl"
)

joblib.dump(
    encoder,
    "models/equipment_encoder.pkl"
)

# -----------------------------
# 8. Results
# -----------------------------

print("\n========== AI RESULTS ==========\n")

print(
    df["ai_anomaly"].value_counts()
)

print("\nAI detected anomalies:")

print(
    df[df["ai_anomaly"] == 1][
        [
            "timestamp",
            "building",
            "room",
            "occupancy",
            "electricity_kwh",
            "water_liters",
            "ac_status",
            "light_status",
            "fan_status"
        ]
    ].head(10)
)

print("\nModel saved successfully!")

print("models/anomaly_model.pkl")
print("models/equipment_encoder.pkl")