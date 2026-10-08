import pandas as pd
import joblib
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# Load dataset
df = pd.read_csv("data/campus_data.csv")

# Load saved AI model and encoder
model = joblib.load("models/anomaly_model.pkl")
encoder = joblib.load("models/equipment_encoder.pkl")

# Encode equipment status
df["equipment_status_encoded"] = encoder.transform(
    df["equipment_status"]
)

# Features used during training
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

# Prepare input data
X = df[features]

# Generate AI predictions
prediction = model.predict(X)

# Convert Isolation Forest output
# -1 = anomaly
#  1 = normal
df["ai_anomaly"] = (prediction == -1).astype(int)

# Actual labels
y_true = df["known_anomaly"]

# AI predictions
y_pred = df["ai_anomaly"]

print("\n========== MODEL EVALUATION ==========\n")

print("Accuracy:",
      round(accuracy_score(y_true, y_pred), 4))

print("Precision:",
      round(precision_score(y_true, y_pred), 4))

print("Recall:",
      round(recall_score(y_true, y_pred), 4))

print("F1 Score:",
      round(f1_score(y_true, y_pred), 4))

print("\n========== CONFUSION MATRIX ==========\n")

cm = confusion_matrix(y_true, y_pred)

print(cm)

print("\n========== CLASSIFICATION REPORT ==========\n")

print(
    classification_report(
        y_true,
        y_pred,
        target_names=["Normal", "Anomaly"]
    )
)

# Save predictions for later project modules
df.to_csv(
    "data/anomaly_results.csv",
    index=False
)

print("\nAI prediction results saved successfully!")
print("data/anomaly_results.csv")