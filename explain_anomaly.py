import pandas as pd
import joblib
import shap

# Load data
df = pd.read_csv("data/root_cause_results.csv")

# Load trained model and encoder
model = joblib.load("models/anomaly_model.pkl")
encoder = joblib.load("models/equipment_encoder.pkl")

# Encode equipment status
df["equipment_status_encoded"] = encoder.transform(
    df["equipment_status"]
)

# Features used by the AI model
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

# Create SHAP explainer
explainer = shap.TreeExplainer(model)

# Calculate SHAP values
shap_values = explainer.shap_values(X)

# Handle SHAP output format
if isinstance(shap_values, list):
    shap_values = shap_values[0]

# Add total importance
df["explanation_score"] = abs(shap_values).sum(axis=1)

# Feature importance for each record
for i, feature in enumerate(features):
    df[f"shap_{feature}"] = shap_values[:, i]


# Find the most important features for each anomaly
def get_top_features(row):

    values = {}

    for feature in features:
        values[feature] = abs(
            row[f"shap_{feature}"]
        )

    sorted_features = sorted(
        values,
        key=values.get,
        reverse=True
    )

    return ", ".join(sorted_features[:3])


df["top_contributing_features"] = df.apply(
    get_top_features,
    axis=1
)


# Save results
df.to_csv(
    "data/explainable_results.csv",
    index=False
)


print("\n========== EXPLAINABLE AI RESULTS ==========\n")

anomalies = df[df["ai_anomaly"] == 1].head(10)

for _, row in anomalies.iterrows():

    print("----------------------------------------")

    print("Room:", row["room"])

    print("Timestamp:", row["timestamp"])

    print("Root Cause:",
          row["root_cause_code"])

    print("Top contributing factors:",
          row["top_contributing_features"])

    print("Electricity:",
          row["electricity_kwh"])

    print("Water:",
          row["water_liters"])

    print("Occupancy:",
          row["occupancy"])

    print("AC:",
          row["ac_status"])

    print("Lights:",
          row["light_status"])


print("\nExplainable AI results saved successfully!")

print("data/explainable_results.csv")