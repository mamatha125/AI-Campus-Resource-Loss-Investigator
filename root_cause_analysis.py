import pandas as pd


# Load AI anomaly results
df = pd.read_csv("data/anomaly_results.csv")


def find_root_cause(row):

    # Case 1: AC running in an empty room
    if (
        row["occupancy"] == 0
        and row["class_scheduled"] == 0
        and row["ac_status"] == 1
    ):
        return (
            "AC_LEFT_ON",
            "Air conditioner is running while the room is unoccupied"
        )

    # Case 2: Lights running in an empty room
    elif (
        row["occupancy"] == 0
        and row["class_scheduled"] == 0
        and row["light_status"] == 1
    ):
        return (
            "LIGHTS_LEFT_ON",
            "Lights are ON while the room is unoccupied"
        )

    # Case 3: High water usage
    elif row["water_liters"] > 8:
        return (
            "POSSIBLE_WATER_LEAK",
            "Unusually high water consumption detected"
        )

    # Case 4: Equipment problem
    elif row["equipment_status"] == "Fault":
        return (
            "EQUIPMENT_FAULT",
            "Equipment fault detected"
        )

    # Case 5: High electricity usage
    elif row["electricity_kwh"] > 5:
        return (
            "HIGH_ELECTRICITY_USAGE",
            "Unusually high electricity consumption detected"
        )

    # No clear cause
    else:
        return (
            "UNKNOWN",
            "Anomaly detected but no clear root cause identified"
        )


# Apply root-cause analysis only to AI anomalies
df["root_cause_code"] = "NORMAL"
df["root_cause_description"] = "No anomaly"

for index, row in df[df["ai_anomaly"] == 1].iterrows():

    cause, description = find_root_cause(row)

    df.loc[index, "root_cause_code"] = cause
    df.loc[index, "root_cause_description"] = description


# Save results
df.to_csv(
    "data/root_cause_results.csv",
    index=False
)


print("\n========== ROOT-CAUSE ANALYSIS ==========\n")

print(
    df[df["ai_anomaly"] == 1][
        [
            "timestamp",
            "building",
            "room",
            "occupancy",
            "class_scheduled",
            "electricity_kwh",
            "water_liters",
            "ac_status",
            "light_status",
            "equipment_status",
            "root_cause_code",
            "root_cause_description"
        ]
    ].head(15).to_string(index=False)
)

print("\n========== ROOT-CAUSE SUMMARY ==========\n")

print(
    df[df["ai_anomaly"] == 1]["root_cause_code"]
    .value_counts()
)

print("\nRoot-cause results saved successfully!")

print("data/root_cause_results.csv")