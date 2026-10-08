import pandas as pd


# Load explainable AI results
df = pd.read_csv("data/explainable_results.csv")


# Calculate baseline electricity
normal_electricity = df[
    df["ai_anomaly"] == 0
]["electricity_kwh"].median()


# Calculate baseline water
normal_water = df[
    df["ai_anomaly"] == 0
]["water_liters"].median()


# Calculate excess resource usage
df["excess_electricity_kwh"] = (
    df["electricity_kwh"] - normal_electricity
).clip(lower=0)


df["excess_water_liters"] = (
    df["water_liters"] - normal_water
).clip(lower=0)


# Calculate combined impact score
df["impact_score"] = (
    df["excess_electricity_kwh"] * 10
    + df["excess_water_liters"] * 2
)


# Assign impact level
def get_impact_level(score):

    if score >= 30:
        return "HIGH"

    elif score >= 10:
        return "MEDIUM"

    else:
        return "LOW"


df["impact_level"] = df["impact_score"].apply(
    get_impact_level
)


# Normal records should not be treated as resource-loss events
df.loc[
    df["ai_anomaly"] == 0,
    [
        "excess_electricity_kwh",
        "excess_water_liters",
        "impact_score",
        "impact_level"
    ]
] = [0, 0, 0, "NORMAL"]


# Save results
df.to_csv(
    "data/impact_results.csv",
    index=False
)


print("\n========== IMPACT ESTIMATION ==========\n")


# Display anomalies
anomalies = df[df["ai_anomaly"] == 1].head(15)


for _, row in anomalies.iterrows():

    print("----------------------------------------")

    print("Room:", row["room"])

    print("Timestamp:", row["timestamp"])

    print("Root Cause:",
          row["root_cause_code"])

    print(
        "Excess Electricity:",
        round(row["excess_electricity_kwh"], 2),
        "kWh"
    )

    print(
        "Excess Water:",
        round(row["excess_water_liters"], 2),
        "liters"
    )

    print(
        "Impact Score:",
        round(row["impact_score"], 2)
    )

    print(
        "Impact Level:",
        row["impact_level"]
    )


print("\n========== IMPACT SUMMARY ==========\n")

print(
    df[df["ai_anomaly"] == 1]["impact_level"]
    .value_counts()
)


print("\nTotal estimated excess electricity:")

print(
    round(
        df[df["ai_anomaly"] == 1]
        ["excess_electricity_kwh"]
        .sum(),
        2
    ),
    "kWh"
)


print("\nTotal estimated excess water:")

print(
    round(
        df[df["ai_anomaly"] == 1]
        ["excess_water_liters"]
        .sum(),
        2
    ),
    "liters"
)


print("\nImpact estimation completed successfully!")

print("data/impact_results.csv")