import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings('ignore')
from modules import data_gen, forecaster, ai_engine, ui_components

# Page Config
st.set_page_config(page_title="Retail Demand AI", page_icon="📈", layout="wide")

# Load CSS
ui_components.load_css()

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # API Key Handling
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key")
    if not api_key:
        st.warning("Please enter API Key to enable AI insights.")
    
    st.markdown("---")
    
    st.subheader("Data Controls")
    if st.button("Regenerate Synthetic Data"):
        with st.spinner("Generating new data..."):
            data_gen.generate_data()
        st.success("Data regenerated!")
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()

# Load Data
@st.cache(suppress_st_warning=True)
def load_data():
    if not os.path.exists("data/sales_history.csv"):
        data_gen.generate_data()
    
    sales = pd.read_csv("data/sales_history.csv")
    inventory = pd.read_csv("data/inventory.csv")
    return sales, inventory

try:
    df_sales, df_inventory = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Main Dashboard
st.title("🚀 Intelligent Demand Forecast & Inventory Manager")
st.markdown("### AI-Powered Insights for Retail Optimization")

# Product Selection
product_list = df_inventory['ProductName'].unique()
selected_product_name = st.selectbox("Select Product to Analyze", product_list)

# Get Product IDs
product_info = df_inventory[df_inventory['ProductName'] == selected_product_name].iloc[0]
product_id = product_info['ProductID']

# 1. Top Level Metrics
col1, col2, col3, col4 = st.columns(4)

stats = forecaster.get_product_stats(df_sales, product_id)

with col1:
    ui_components.metric_card("Current Stock", product_info['CurrentStock'])
with col2:
    ui_components.metric_card("Reorder Level", product_info['ReorderLevel'])
with col3:
    ui_components.metric_card("Avg Price", f"${stats['avg_price']:.2f}")
with col4:
    status = "🟢 OK" if product_info['CurrentStock'] > product_info['ReorderLevel'] else "🔴 LOW STOCK"
    ui_components.metric_card("Status", status)

st.markdown("---")

# 2. Forecast Section
st.subheader("📉 Demand Forecast")

history_df, forecast_df = forecaster.calculate_forecast(df_sales, product_id)

# Plotly Chart
fig = go.Figure()

# Historical Data
fig.add_trace(go.Scatter(
    x=history_df['Date'], 
    y=history_df['Actual'],
    mode='lines',
    name='Historical Sales',
    line=dict(color='#4c72b0', width=2)
))

# Smoothed Trend
fig.add_trace(go.Scatter(
    x=history_df['Date'], 
    y=history_df['Smoothed'],
    mode='lines',
    name='Trend (Smoothed)',
    line=dict(color='#dd8452', width=2, dash='dash')
))

# Forecast
fig.add_trace(go.Scatter(
    x=forecast_df['Date'], 
    y=forecast_df['Forecast'],
    mode='lines',
    name='Forecast (Next 30 Days)',
    line=dict(color='#55a868', width=3)
))

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="Units Sold",
    height=400,
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(orientation="h", y=1.1)
)

st.plotly_chart(fig, use_container_width=True)

# 3. AI Explanation & Recommendations
st.subheader("🤖 AI Analyst Insights")

col_ai, col_actions = st.columns([2, 1])

with col_ai:
    if st.button("Generate Explanation"):
        with st.spinner("Analyzing patterns and consulting AI..."):
            # Prepare summaries for AI
            hist_summary = f"Last 30 days total: {stats['last_30_days_sales']} units."
            forecast_val = int(forecast_df['Forecast'].mean())
            forecast_summary = f"Predicted avg daily demand: {forecast_val} units."
            inv_summary = f"Current: {product_info['CurrentStock']}, Reorder Level: {product_info['ReorderLevel']}"
            
            explanation = ai_engine.generate_explanation(
                selected_product_name, 
                hist_summary, 
                forecast_summary, 
                inv_summary, 
                api_key
            )
            
            st.markdown(f"""
            <div class="explanation-box">
                {explanation}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Click 'Generate Explanation' to get AI-driven insights on this forecast.")

with col_actions:
    st.markdown("### ⚡ Recommended Actions")
    
    # Simple rule-based recommendations to complement AI
    if product_info['CurrentStock'] <= product_info['ReorderLevel']:
        st.error(f"⚠️ **Restock Needed!**\nStock is below reorder level ({product_info['ReorderLevel']}).")
        if st.button(f"Order {product_info['ReorderLevel'] * 2} Units"):
            st.success("Order request sent to supplier!")
    else:
        st.success("✅ Inventory Healthy")
        
    if stats['last_30_days_sales'] < 10: # Low sales
        st.warning("📉 **Slow Moving**\nConsider a promotion.")
        if st.button("Launch 10% Off Promo"):
            st.success("Promotion scheduled!")

st.markdown("---")
st.caption("Powered by Google Gemini & ChromaDB | Local Caching Enabled for Cost Efficiency")
