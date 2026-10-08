import pandas as pd


# ==========================================
# 1. Load recommendation results
# ==========================================

df = pd.read_csv("data/recommendation_results.csv")

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort records by room and time
df = df.sort_values(["room", "timestamp"]).reset_index(drop=True)


# ==========================================
# 2. Calculate previous resource usage
# ==========================================

df["previous_electricity"] = (
    df.groupby("room")["electricity_kwh"]
    .shift(1)
)

df["previous_water"] = (
    df.groupby("room")["water_liters"]
    .shift(1)
)


# ==========================================
# 3. Calculate change after anomaly
# ==========================================

df["electricity_reduction"] = (
    df["previous_electricity"]
    - df["electricity_kwh"]
)

df["water_reduction"] = (
    df["previous_water"]
    - df["water_liters"]
)


# ==========================================
# 4. Calculate percentage reduction
# ==========================================

df["electricity_reduction_percent"] = (
    df["electricity_reduction"]
    / df["previous_electricity"]
    * 100
)

df["water_reduction_percent"] = (
    df["water_reduction"]
    / df["previous_water"]
    * 100
)


# ==========================================
# 5. Handle missing values
# ==========================================

df["electricity_reduction_percent"] = (
    df["electricity_reduction_percent"]
    .fillna(0)
)

df["water_reduction_percent"] = (
    df["water_reduction_percent"]
    .fillna(0)
)


# ==========================================
# 6. Verify resolution
# ==========================================

def verify_resolution(row):

    # Normal records
    if row["ai_anomaly"] == 0:
        return "NOT_APPLICABLE"

    electricity_improved = (
        row["electricity_reduction_percent"] >= 10
    )

    water_improved = (
        row["water_reduction_percent"] >= 10
    )

    # If either resource improved significantly
    if electricity_improved or water_improved:
        return "RESOLVED"

    return "NOT_RESOLVED"


df["resolution_status"] = df.apply(
    verify_resolution,
    axis=1
)


# ==========================================
# 7. Save resolution results
# ==========================================

df.to_csv(
    "data/resolution_results.csv",
    index=False
)


# ==========================================
# 8. Display results
# ==========================================

print("\n========== RESOLUTION VERIFICATION ==========\n")

anomalies = df[
    df["ai_anomaly"] == 1
].head(15)


for _, row in anomalies.iterrows():

    print("----------------------------------------")

    print("Room:", row["room"])

    print("Timestamp:", row["timestamp"])

    print(
        "Root Cause:",
        row["root_cause_code"]
    )

    print(
        "Impact Level:",
        row["impact_level"]
    )

    print(
        "Recommendation:",
        row["recommendation"]
    )

    print(
        "Electricity Reduction:",
        round(
            row["electricity_reduction_percent"],
            2
        ),
        "%"
    )

    print(
        "Water Reduction:",
        round(
            row["water_reduction_percent"],
            2
        ),
        "%"
    )

    print(
        "Resolution Status:",
        row["resolution_status"]
    )


# ==========================================
# 9. Summary
# ==========================================

print("\n========== RESOLUTION SUMMARY ==========\n")

print(
    df[
        df["ai_anomaly"] == 1
    ]["resolution_status"].value_counts()
)


print("\nResolution verification completed successfully!")

print("Output: data/resolution_results.csv")