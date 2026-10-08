import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

rows = []

buildings = ["Block_A", "Block_B", "Block_C"]

rooms = [
    "A101", "A102", "A103",
    "B201", "B202", "B203",
    "C301", "C302", "C303"
]

dates = pd.date_range(
    start="2026-01-01",
    end="2026-03-31",
    freq="h"
)

for timestamp in dates:

    hour = timestamp.hour

    for room in rooms:

        building = room[0]

        # College operating hours
        college_hours = 9 <= hour <= 16

        # Occupancy
        if college_hours:
            occupancy = np.random.randint(15, 61)
        else:
            occupancy = np.random.choice([0, 0, 0, 1, 2])

        # Class schedule
        if college_hours and occupancy > 5:
            class_scheduled = np.random.choice([0, 1], p=[0.2, 0.8])
        else:
            class_scheduled = 0

        # Temperature
        temperature = round(
            np.random.normal(28, 2),
            1
        )

        # Equipment
        equipment_status = np.random.choice(
            ["Normal", "Normal", "Normal", "Maintenance"]
        )

        # AC
        if temperature > 26 and (occupancy > 5 or class_scheduled == 1):
            ac_status = 1
        else:
            ac_status = 0

        # Lights
        if occupancy > 0:
            light_status = 1
        else:
            light_status = np.random.choice([0, 1], p=[0.8, 0.2])

        # Fans
        if occupancy > 0:
            fan_status = 1
        else:
            fan_status = np.random.choice([0, 1], p=[0.85, 0.15])

        # Base electricity
        electricity = 0.8

        electricity += occupancy * 0.025
        electricity += ac_status * 1.8
        electricity += light_status * 0.6
        electricity += fan_status * 0.4

        # Equipment effect
        if equipment_status == "Maintenance":
            electricity += 0.8

        electricity += np.random.normal(0, 0.15)

        # Water usage
        water = (
            1.5
            + occupancy * 0.08
            + np.random.normal(0, 0.2)
        )

        # Occasionally create hidden resource-loss events
        anomaly = 0

        if np.random.random() < 0.025:

            anomaly = 1

            anomaly_type = np.random.choice([
                "AC_LEFT_ON",
                "LIGHTS_LEFT_ON",
                "WATER_LEAK",
                "EQUIPMENT_FAULT"
            ])

            if anomaly_type == "AC_LEFT_ON":
                occupancy = 0
                class_scheduled = 0
                ac_status = 1
                electricity += np.random.uniform(2.0, 4.0)

            elif anomaly_type == "LIGHTS_LEFT_ON":
                occupancy = 0
                class_scheduled = 0
                light_status = 1
                electricity += np.random.uniform(1.0, 2.0)

            elif anomaly_type == "WATER_LEAK":
                water += np.random.uniform(15, 40)

            elif anomaly_type == "EQUIPMENT_FAULT":
                equipment_status = "Fault"
                electricity += np.random.uniform(2.0, 5.0)

        rows.append({
            "timestamp": timestamp,
            "building": building,
            "room": room,
            "occupancy": occupancy,
            "class_scheduled": class_scheduled,
            "temperature": temperature,
            "electricity_kwh": round(max(electricity, 0), 2),
            "water_liters": round(max(water, 0), 2),
            "equipment_status": equipment_status,
            "ac_status": ac_status,
            "light_status": light_status,
            "fan_status": fan_status,
            "known_anomaly": anomaly
        })


df = pd.DataFrame(rows)

output_path = Path("data/campus_data.csv")

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False
)

print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_path}")

print("\nAnomalies:")
print(df["known_anomaly"].value_counts())

print("\nFirst 5 rows:")
print(df.head())