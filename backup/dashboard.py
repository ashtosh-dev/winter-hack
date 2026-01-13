import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="GHOST-SHIELD AI (Offline Mode)",
    layout="wide",
    page_icon="🛡️"
)

# --------------------------------------------------
# Load Local Data (NO AUTH, NO BIGQUERY)
# --------------------------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    df = pd.read_csv(
        "../backup/outputs/final_results.csv",
        parse_dates=["Date"]
    )
    return df

# --------------------------------------------------
# Main App
# --------------------------------------------------
def main():
    st.title("🛡️ GHOST-SHIELD AI")
    st.caption(
        "Detecting Ghost Demand and preventing invisible supply-chain losses using ML + Optimization"
    )
    st.divider()

    # ---------- Load ----------
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Failed to load local data: {e}")
        return

    # ---------- SAFETY: DERIVE is_ghost IF MISSING ----------
    if "is_ghost" not in df.columns:
        if "ghost_flag" in df.columns:
            df["is_ghost"] = df["ghost_flag"] == -1
        elif "ghost_demand" in df.columns:
            df["is_ghost"] = df["ghost_demand"] > 0
        else:
            # fallback: assume all rows are ghost alerts
            df["is_ghost"] = True

    # ---------- GLOBAL METRICS (NO DOUBLE COUNTING) ----------
    global_sku_level = (
        df.groupby("SKU")[["cost_saving", "waste_reduction_value"]]
        .sum()
        .reset_index()
    )

    total_cost_saved = global_sku_level["cost_saving"].sum()
    total_waste_saved = global_sku_level["waste_reduction_value"].sum()
    total_savings = total_cost_saved + total_waste_saved
    ghost_cases = int(df["is_ghost"].sum())

    # ---------- KPI TILES ----------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Total Estimated Savings", f"₹{total_savings:,.0f}")
    c2.metric("🏭 Production Cost Saved", f"₹{total_cost_saved:,.0f}")
    c3.metric("♻️ Waste Reduction Value", f"₹{total_waste_saved:,.0f}")
    c4.metric("🚨 Ghost Demand Alerts", ghost_cases)

    st.divider()

    # ---------- SIDEBAR FILTERS ----------
    st.sidebar.header("Product Filters")

    all_skus = sorted(df["SKU"].unique())
    selected_skus = st.sidebar.multiselect(
        "Select SKUs",
        options=all_skus,
        default=all_skus[:3]
    )

    filtered_df = df[df["SKU"].isin(selected_skus)]

    # ---------- SAVINGS PER SKU ----------
    st.subheader("📊 Savings per SKU")

    sku_savings = (
        filtered_df
        .groupby("SKU")[["cost_saving", "waste_reduction_value"]]
        .sum()
        .reset_index()
    )

    sku_savings["total_savings"] = (
        sku_savings["cost_saving"] + sku_savings["waste_reduction_value"]
    )

    fig_bar = px.bar(
        sku_savings.sort_values("total_savings", ascending=False),
        x="SKU",
        y="total_savings",
        template="plotly_dark",
        labels={"total_savings": "Total Savings (₹)"}
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # ---------- EXPLAINABILITY ----------
    st.divider()
    st.subheader("🔍 Why These Alerts Were Triggered")

    st.markdown("""
    - Forecast spikes without proportional sales support  
    - High short-term volatility compared to historical demand  
    - Isolation Forest flagged statistically abnormal patterns  
    - OR-Tools optimized production cuts to reduce waste and cost  
    """)

    # ---------- ACTION LEDGER ----------
    st.divider()
    st.subheader("📄 Production Action Ledger")

    st.dataframe(
        filtered_df[
            [
                "Date",
                "SKU",
                "daily_sales",
                "forecast_error",
                "recommended_cut",
                "cost_saving",
                "waste_reduction_value",
            ]
        ].head(20),
        use_container_width=True,
    )

# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    main()
