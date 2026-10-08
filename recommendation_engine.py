import pandas as pd


# ==========================================
# 1. Load impact estimation results
# ==========================================

df = pd.read_csv("data/impact_results.csv")


# ==========================================
# 2. Recommendation function
# ==========================================

def generate_recommendation(root_cause, impact_level):

    if root_cause == "POSSIBLE_WATER_LEAK":

        if impact_level == "HIGH":
            return (
                "Immediately inspect plumbing, taps and pipelines "
                "for possible water leakage."
            )
        else:
            return (
                "Inspect water outlets and plumbing for abnormal usage."
            )

    elif root_cause == "AC_LEFT_ON":

        if impact_level == "HIGH":
            return (
                "Immediately check the AC and switch it off when "
                "the room is unoccupied."
            )
        else:
            return (
                "Check whether the AC is being left ON when the room "
                "is unoccupied."
            )

    elif root_cause == "HIGH_ELECTRICITY_USAGE":

        if impact_level == "HIGH":
            return (
                "Inspect high-power electrical equipment and reduce "
                "unnecessary electricity consumption."
            )
        else:
            return (
                "Monitor electrical equipment and switch off "
                "unnecessary devices."
            )

    elif root_cause == "EQUIPMENT_FAULT":

        if impact_level == "HIGH":
            return (
                "Inspect the equipment immediately for possible "
                "fault or abnormal power consumption."
            )
        else:
            return (
                "Schedule equipment inspection and monitor "
                "its electricity consumption."
            )

    elif root_cause == "UNKNOWN":

        return (
            "Inspect the room and monitor electricity and water "
            "usage to identify the possible cause."
        )

    else:

        return (
            "Monitor the room and investigate the abnormal "
            "resource consumption."
        )


# ==========================================
# 3. Generate recommendations
# ==========================================

df["recommendation"] = df.apply(
    lambda row: generate_recommendation(
        row["root_cause_code"],
        row["impact_level"]
    ),
    axis=1
)


# ==========================================
# 4. Priority
# ==========================================

def assign_priority(impact_level):

    if impact_level == "HIGH":
        return "URGENT"

    elif impact_level == "MEDIUM":
        return "ACTION_REQUIRED"

    elif impact_level == "LOW":
        return "MONITOR"

    else:
        return "NO_ACTION"


df["priority"] = df["impact_level"].apply(
    assign_priority
)


# ==========================================
# 5. Normal records
# ==========================================

df.loc[
    df["ai_anomaly"] == 0,
    ["recommendation", "priority"]
] = [
    "No action required. Resource usage is normal.",
    "NO_ACTION"
]


# ==========================================
# 6. Save results
# ==========================================

df.to_csv(
    "data/recommendation_results.csv",
    index=False
)


# ==========================================
# 7. Display recommendations
# ==========================================

print("\n========== RECOMMENDATION ENGINE ==========\n")


anomalies = df[
    df["ai_anomaly"] == 1
].head(15)


for _, row in anomalies.iterrows():

    print("----------------------------------------")

    print("Room:", row["room"])

    print("Timestamp:", row["timestamp"])

    print("Root Cause:", row["root_cause_code"])

    print("Impact Level:", row["impact_level"])

    print("Priority:", row["priority"])

    print("Recommendation:")

    print(row["recommendation"])


# ==========================================
# 8. Recommendation summary
# ==========================================

print("\n========== PRIORITY SUMMARY ==========\n")

print(
    df[df["ai_anomaly"] == 1]["priority"]
    .value_counts()
)


print("\n========== ROOT CAUSE SUMMARY ==========\n")

print(
    df[df["ai_anomaly"] == 1]["root_cause_code"]
    .value_counts()
)


print("\nRecommendation engine completed successfully!")

print("Output: data/recommendation_results.csv")