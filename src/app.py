# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# import plotly.express as px
# import os

# # Page Config
# st.set_page_config(
#     page_title="Ghost Demand Mitigation Dashboard",
#     page_icon="👻",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for Premium Look
# st.markdown("""
#     <style>
#     .main {
#         background-color: #0e1117;
#     }
#     .stMetric {
#         background-color: #1e2130;
#         padding: 15px;
#         border-radius: 10px;
#         border: 1px solid #3d4455;
#     }
#     [data-testid="stSidebar"] {
#         background-color: #161b22;
#     }
#     h1, h2, h3 {
#         color: #ffffff;
#         font-family: 'Inter', sans-serif;
#     }
#     </style>
# """, unsafe_allow_html=True)

# def load_data():
#     path = "data/processed_demand.csv"
#     if not os.path.exists(path):
#         st.error(f"Data file not found at {path}. Please run `src/main.py` first.")
#         return None
#     df = pd.read_csv(path)
#     df['date'] = pd.to_datetime(df['date'])
#     return df

# def main():
#     st.title("👻 Ghost Demand Mitigation Engine")
#     st.markdown("---")

#     df = load_data()
#     if df is None:
#         return

#     # Sidebar
#     st.sidebar.header("Settings")
#     show_raw = st.sidebar.checkbox("Show Raw Data", False)
    
#     # Metrics
#     total_waste_blind = df['overproduction_waste'].sum()
#     optimized_waste = (df['optimized_production'] - df['real_demand']).clip(lower=0).sum()
#     savings = total_waste_blind - optimized_waste
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Total Ghost Demand Signal", f"{df['ghost_demand'].sum():,.0f} units")
#     with col2:
#         st.metric("Waste Saved (Optimized)", f"{savings:,.0f} units", delta=f"{ (savings/total_waste_blind)*100:.1f}%")
#     with col3:
#         st.metric("Anomaly Detection Accuracy", "94.2%") # Simplified for demo

#     st.markdown("### 📈 Supply Chain Performance Analysis")

#     # Demand vs Filtered Chart
#     fig = go.Figure()
    
#     # Raw Signal
#     fig.add_trace(go.Scatter(
#         x=df['date'], y=df['total_demand'],
#         name="Raw Demand Signal (with Ghosts)",
#         line=dict(color='#ff4b4b', width=1.5, dash='dot'),
#         opacity=0.6
#     ))
    
#     # Real Market Demand
#     fig.add_trace(go.Scatter(
#         x=df['date'], y=df['real_demand'],
#         name="Actual Market Need",
#         line=dict(color='#00d4ff', width=2)
#     ))

#     # ML Filtered Signal
#     fig.add_trace(go.Scatter(
#         x=df['date'], y=df['filtered_demand'],
#         name="ML Filtered Demand (Clean)",
#         line=dict(color='#00ff9d', width=3)
#     ))

#     fig.update_layout(
#         template="plotly_dark",
#         height=500,
#         margin=dict(l=20, r=20, t=40, b=20),
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#         hovermode="x unified"
#     )
#     st.plotly_chart(fig, width='stretch')

#     st.markdown("### 🛠 Production Planning (OR-Tools vs Blind)")
    
#     col_a, col_b = st.columns(2)
    
#     with col_a:
#         st.subheader("Blind Planning (Status Quo)")
#         st.write("Production follows every spike immediately.")
#         fig_blind = px.line(df, x="date", y=["total_demand", "blind_production"], 
#                            color_discrete_map={"total_demand": "#ff4b4b", "blind_production": "#ffffff"},
#                            template="plotly_dark")
#         st.plotly_chart(fig_blind, width='stretch')
        
#     with col_b:
#         st.subheader("Optimized Planning (Proposed)")
#         st.write("Production is smoothed and ignores Ghost Demand.")
#         fig_opt = px.line(df, x="date", y=["real_demand", "optimized_production"],
#                          color_discrete_map={"real_demand": "#00d4ff", "optimized_production": "#00ff9d"},
#                          template="plotly_dark")
#         st.plotly_chart(fig_opt, width='stretch')

#     if show_raw:
#         st.markdown("### 📄 Raw Processed Data")
#         st.dataframe(df, width='stretch')

# if __name__ == "__main__":
#     main()



import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Ghost Demand Intelligence System",
    page_icon="📦",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        "../outputs/final_results.csv",
        parse_dates=["Date"]
    )


df = load_data()
ghost_df = df[df["ghost_demand"] == 1]

# -----------------------------
# Header
# -----------------------------
st.title("📦 Ghost Demand Intelligence System")

st.markdown("""
**Problem:** Businesses overproduce by trusting inflated demand signals.  
**Solution:** Detect ghost demand and compute optimal production cuts to reduce cost and waste.
""")

st.divider()

# -----------------------------
# KPIs
# -----------------------------
# -----------------------------
# KPIs (Clean & Business-Focused)
# -----------------------------
# -----------------------------
# KPIs (Final Business View)
# -----------------------------
total_units_reduced = ghost_df['recommended_cut'].sum()
production_cost_saved = ghost_df['cost_saving'].sum()
waste_saved = ghost_df['waste_reduction_value'].sum()
total_cost_saved = production_cost_saved + waste_saved

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Ghost Demand Cases",
    f"{len(ghost_df):,}"
)

col2.metric(
    "Total Units Reduced",
    f"{total_units_reduced:,.0f}"
)

col3.metric(
    "Total Cost Saved",
    f"₹{total_cost_saved:,.0f}"
)

col4.metric(
    "Waste Reduction Value",
    f"₹{waste_saved:,.0f}"
)


# -----------------------------
# Explanation
# -----------------------------
st.subheader("🧠 How It Works")

st.markdown("""
- Expected demand is inferred from recent historical sales  
- Large deviations from actual sales indicate **ghost demand**  
- **Isolation Forest** detects abnormal demand behavior  
- **OR-Tools optimization** recommends safe production cuts  
""")

st.divider()

# -----------------------------
# Top Risk Table
# -----------------------------
st.subheader("⚠️ Highest Ghost Demand Risks")

top_cases = (
    ghost_df
    .sort_values("forecast_error", ascending=False)
    .head(10)
)

st.dataframe(
    top_cases[[
        "Date",
        "SKU",
        "daily_sales",
        "rolling_mean_7",
        "forecast_error",
        "recommended_cut",
        "cost_saving"
    ]],
    use_container_width=True
)

st.divider()

# -----------------------------
# SKU Explorer
# -----------------------------
st.subheader("🔍 SKU-Level View")

sku = st.selectbox(
    "Select SKU",
    ghost_df["SKU"].unique()
)

sku_df = ghost_df[ghost_df["SKU"] == sku]

st.line_chart(
    sku_df.set_index("Date")[["daily_sales", "rolling_mean_7"]],
    height=300
)

st.caption("Actual Sales vs Expected Demand")

st.divider()

# -----------------------------
# Footer
# -----------------------------
st.caption(
    "Ghost Demand Intelligence System • Backup Demo UI • Hackathon Submission"
)
