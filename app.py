# import streamlit as st
# import pandas as pd
# import pandas_gbq
# import plotly.express as px

# from src.data_cleaning import load_data
# from src.feature_engineering import add_time_series_features
# from src.ml_model import load_ghost_model, detect_ghost_demand

# # --------------------------------------------------
# # Page Config
# # --------------------------------------------------
# st.set_page_config(
#     page_title="GHOST-SHIELD AI",
#     layout="wide",
#     page_icon="🛡️"
# )

# # --------------------------------------------------
# # Config
# # --------------------------------------------------
# PROJECT_ID = "ghost-demand-hackathon"
# BQ_TABLE = "supply_chain_data.ghost_demand_alerts"

# # --------------------------------------------------
# # Load Data
# # --------------------------------------------------
# @st.cache_data(show_spinner=True)
# def load_data():
#     query = f"SELECT * FROM `{BQ_TABLE}`"
#     df = pandas_gbq.read_gbq(query, project_id=PROJECT_ID)
#     df["Date"] = pd.to_datetime(df["Date"])
#     return df


# # --------------------------------------------------
# # Main App
# # --------------------------------------------------
# def main():
#     st.title("🛡️ GHOST-SHIELD AI")
#     st.caption(
#         "Detecting Ghost Demand and preventing invisible supply-chain losses using ML + Optimization"
#     )
#     st.divider()

#     # ---------- Load ----------
#     try:
#         df = load_data()
#     except Exception as e:
#         st.error(f"Failed to load data: {e}")
#         return

#     # ---------- GLOBAL METRICS (NO DOUBLE COUNTING) ----------
#     global_sku_level = (
#         df.groupby("SKU")[["cost_saving", "waste_reduction_value"]]
#         .sum()
#         .reset_index()
#     )

#     total_cost_saved = global_sku_level["cost_saving"].sum()
#     total_waste_saved = global_sku_level["waste_reduction_value"].sum()
#     total_savings = total_cost_saved + total_waste_saved
#     ghost_cases = df.shape[0]

#     # ---------- KPI TILES ----------
#     c1, c2, c3, c4 = st.columns(4)

#     c1.metric("💰 Total Estimated Savings", f"₹{total_savings:,.0f}")
#     c2.metric("🏭 Production Cost Saved", f"₹{total_cost_saved:,.0f}")
#     c3.metric("♻️ Waste Reduction Value", f"₹{total_waste_saved:,.0f}")
#     c4.metric("🚨 Ghost Demand Alerts", ghost_cases)

#     st.divider()

#     # ---------- SIDEBAR FILTERS ----------
#     st.sidebar.header("Product Filters")

#     all_skus = sorted(df["SKU"].unique())
#     selected_skus = st.sidebar.multiselect(
#         "Select SKUs",
#         options=all_skus,
#         default=all_skus[:3]
#     )

#     filtered_df = df[df["SKU"].isin(selected_skus)]

#     # ---------- SAVINGS PER SKU ----------
#     st.subheader("📊 Savings per SKU")

#     sku_savings = (
#         filtered_df
#         .groupby("SKU")[["cost_saving", "waste_reduction_value"]]
#         .sum()
#         .reset_index()
#     )

#     sku_savings["total_savings"] = (
#         sku_savings["cost_saving"] + sku_savings["waste_reduction_value"]
#     )

#     fig_bar = px.bar(
#         sku_savings.sort_values("total_savings", ascending=False),
#         x="SKU",
#         y="total_savings",
#         template="plotly_dark",
#         labels={"total_savings": "Total Savings (₹)"}
#     )

#     st.plotly_chart(fig_bar, use_container_width=True)

#     # ---------- EXPLAINABILITY ----------
#     st.divider()
#     st.subheader("🔍 Why These Alerts Were Triggered")

#     st.markdown("""
#     - Forecast spikes without proportional sales
#     - High short-term volatility vs historical demand
#     - Isolation Forest flagged abnormal demand patterns
#     - OR-Tools optimized production cuts to reduce waste and cost
#     """)

#     # ---------- ACTION LEDGER ----------
#     st.divider()
#     st.subheader("📄 Production Action Ledger")

#     st.dataframe(
#         filtered_df[
#             [
#                 "Date",
#                 "SKU",
#                 "daily_sales",
#                 "forecast_error",
#                 "recommended_cut",
#                 "cost_saving",
#                 "waste_reduction_value",
#             ]
#         ].head(20),
#         use_container_width=True,
#     )


# # --------------------------------------------------
# # Run
# # --------------------------------------------------
# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="GHOST-SHIELD AI",
    layout="wide",
    page_icon="🛡️"
)

# --------------------------------------------------
# Load Precomputed Ghost Demand Results
# --------------------------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    df = pd.read_csv("data/ghost_demand_results.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


# --------------------------------------------------
# Main App
# --------------------------------------------------
def main():
    st.title("🛡️ GHOST-SHIELD AI")
    st.caption(
        "Detecting ghost demand and preventing invisible supply-chain losses using ML"
    )
    st.divider()

    # ---------- Load ----------
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Failed to load ghost demand data: {e}")
        return

    if df.empty:
        st.warning("No ghost demand records available.")
        return

    # ---------- GLOBAL METRICS ----------
    total_cases = df.shape[0]
    total_units = int(df["daily_sales"].sum())

    c1, c2 = st.columns(2)
    c1.metric("🚨 Ghost Demand Cases", total_cases)
    c2.metric("📦 Units Affected", total_units)

    st.divider()

    # ---------- SIDEBAR FILTER ----------
    st.sidebar.header("Product Filters")

    all_skus = sorted(df["SKU"].unique())
    selected_skus = st.sidebar.multiselect(
        "Select SKUs",
        options=all_skus,
        default=all_skus[:3]
    )

    filtered_df = df[df["SKU"].isin(selected_skus)]

    if filtered_df.empty:
        st.warning("No records for selected SKUs.")
        return

    # ---------- CHART ----------
    st.subheader("📊 Ghost Demand by SKU")

    sku_counts = (
        filtered_df.groupby("SKU")
        .size()
        .reset_index(name="ghost_cases")
        .sort_values("ghost_cases", ascending=False)
    )

    fig = px.bar(
        sku_counts,
        x="SKU",
        y="ghost_cases",
        labels={"ghost_cases": "Ghost Demand Alerts"},
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------- EXPLAINABILITY ----------
    st.divider()
    st.subheader("🔍 Why These Alerts Were Triggered")

    st.markdown("""
    - Sudden demand spikes not backed by historical sales  
    - High short-term volatility compared to rolling averages  
    - Forecast error diverging from realized demand  
    - Isolation Forest detected abnormal demand patterns  
    """)

    # ---------- DATA TABLE ----------
    st.divider()
    st.subheader("📄 Ghost Demand Records")

    st.dataframe(
        filtered_df[
            [
                "Date",
                "SKU",
                "daily_sales",
                "forecast_error",
                "volatility_ratio",
                "ghost_demand"
            ]
        ].head(25),
        use_container_width=True
    )


# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    main()

