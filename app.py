import streamlit as st
import pandas as pd


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Campus Resource Investigator",
    page_icon="🏫",
    layout="wide"
)


# ==========================================
# 2. TITLE
# ==========================================

st.title("🏫 AI-Powered Campus Resource Loss Investigator")

st.write(
    "AI system for detecting abnormal campus resource usage, "
    "investigating probable causes, recommending actions, "
    "and verifying whether the issue has been resolved."
)


# ==========================================
# 3. LOAD DATA
# ==========================================

try:

    df = pd.read_csv("data/resolution_results.csv")

except FileNotFoundError:

    st.error(
        "resolution_results.csv not found. "
        "Please run the complete AI pipeline first."
    )

    st.stop()


# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🔎 Filters")

rooms = sorted(df["room"].dropna().unique())

selected_room = st.sidebar.selectbox(
    "Select Room",
    ["All Rooms"] + rooms
)

impact_levels = sorted(
    df["impact_level"].dropna().unique()
)

selected_impact = st.sidebar.selectbox(
    "Impact Level",
    ["All"] + impact_levels
)


# ==========================================
# 5. APPLY FILTERS
# ==========================================

filtered_df = df.copy()

if selected_room != "All Rooms":

    filtered_df = filtered_df[
        filtered_df["room"] == selected_room
    ]

if selected_impact != "All":

    filtered_df = filtered_df[
        filtered_df["impact_level"] == selected_impact
    ]


# ==========================================
# 6. ANOMALIES
# ==========================================

anomalies = filtered_df[
    filtered_df["ai_anomaly"] == 1
]


# ==========================================
# 7. KPI CALCULATIONS
# ==========================================

total_anomalies = len(anomalies)

total_electricity = anomalies[
    "excess_electricity_kwh"
].sum()

total_water = anomalies[
    "excess_water_liters"
].sum()

resolved = len(
    anomalies[
        anomalies["resolution_status"] == "RESOLVED"
    ]
)

not_resolved = len(
    anomalies[
        anomalies["resolution_status"] == "NOT_RESOLVED"
    ]
)


# ==========================================
# 8. KPI CARDS
# ==========================================

st.subheader("📊 Campus Resource Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🚨 Anomalies",
        total_anomalies
    )

with col2:
    st.metric(
        "⚡ Excess Electricity",
        f"{total_electricity:.2f} kWh"
    )

with col3:
    st.metric(
        "💧 Excess Water",
        f"{total_water:.2f} L"
    )

with col4:
    st.metric(
        "✅ Resolved",
        resolved
    )

with col5:
    st.metric(
        "❌ Not Resolved",
        not_resolved
    )


# ==========================================
# 9. IMPACT ANALYSIS
# ==========================================

st.subheader("🚨 Impact Analysis")

col1, col2 = st.columns(2)

with col1:

    st.write("Impact Level Distribution")

    impact_counts = anomalies[
        "impact_level"
    ].value_counts()

    st.bar_chart(impact_counts)


with col2:

    st.write("Root Cause Distribution")

    root_causes = anomalies[
        "root_cause_code"
    ].value_counts()

    st.bar_chart(root_causes)


# ==========================================
# 10. RESOURCE WASTAGE
# ==========================================

st.subheader("⚡💧 Resource Wastage")

resource_data = pd.DataFrame(
    {
        "Resource": [
            "Electricity (kWh)",
            "Water (Liters)"
        ],
        "Excess Usage": [
            total_electricity,
            total_water
        ]
    }
)

st.bar_chart(
    resource_data.set_index("Resource")
)


# ==========================================
# 11. RESOLUTION ANALYSIS
# ==========================================

st.subheader("🔧 Resolution Verification")

resolution_counts = anomalies[
    "resolution_status"
].value_counts()

st.bar_chart(resolution_counts)


# ==========================================
# 12. ANOMALY DETAILS
# ==========================================

st.subheader("🔍 Detected Resource Loss Events")

display_columns = [
    "room",
    "timestamp",
    "root_cause_code",
    "impact_level",
    "priority",
    "excess_electricity_kwh",
    "excess_water_liters",
    "recommendation",
    "resolution_status"
]

available_columns = [
    col for col in display_columns
    if col in anomalies.columns
]

st.dataframe(
    anomalies[available_columns],
    use_container_width=True
)


# ==========================================
# 13. HIGH PRIORITY EVENTS
# ==========================================

st.subheader("🚨 High Priority Events")

high_priority = anomalies[
    anomalies["priority"] == "URGENT"
]

if len(high_priority) > 0:

    st.dataframe(
        high_priority[available_columns],
        use_container_width=True
    )

else:

    st.success(
        "No urgent resource-loss events found."
    )


# ==========================================
# 14. AI RECOMMENDATIONS
# ==========================================

st.subheader("💡 AI Recommendations")

recommendation_columns = [
    "room",
    "root_cause_code",
    "impact_level",
    "priority",
    "recommendation"
]

available_recommendation_columns = [
    col for col in recommendation_columns
    if col in anomalies.columns
]

st.dataframe(
    anomalies[
        available_recommendation_columns
    ],
    use_container_width=True
)


# ==========================================
# 15. FOOTER
# ==========================================

st.divider()

st.success(
    "AI analysis pipeline completed: "
    "Anomaly Detection → Root Cause Analysis → "
    "Impact Estimation → Recommendation → "
    "Resolution Verification"
)

st.caption(
    "AI Campus Resource Loss Investigator | Ideathon Project"
)