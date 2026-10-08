import pandas as pd

# Load dataset
df = pd.read_csv("data/campus_data.csv")

print("\n========== DATASET INFORMATION ==========\n")

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\n========== MISSING VALUES ==========\n")

print(df.isnull().sum())

print("\n========== ANOMALY COUNT ==========\n")

print(df["known_anomaly"].value_counts())

print("\n========== NORMAL RECORD ==========\n")

print(df[df["known_anomaly"] == 0].head(3))

print("\n========== ANOMALY RECORD ==========\n")

print(df[df["known_anomaly"] == 1].head(5))

print("\n========== AVERAGE ELECTRICITY ==========\n")

print(
    df.groupby("known_anomaly")["electricity_kwh"].mean()
)

print("\n========== AVERAGE WATER ==========\n")

print(
    df.groupby("known_anomaly")["water_liters"].mean()
)