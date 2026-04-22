import streamlit as st
import plotly.express as px
import pandas as pd
import os

# Internal modules - Optimized for professional documentation
from utils.analysis import (
    load_data, 
    validate_data_schema, 
    calculate_kpi_metrics, 
    get_market_leaders, 
    get_performance_ranking
)
from utils.recommendation import run_recommendation_engine

# --- INITIALIZATION & UI CONFIG ---
st.set_page_config(page_title="Scalable AI-Driven BI Dashboard", layout="wide", page_icon="📊")

# Custom CSS for Professional White/Light Branding
st.markdown("""
    <style>
    /* Main background and text colors */
    .main { background-color: #f8f9fa; }
    .main-title { font-size: 38px; font-weight: bold; color: #007BFF; text-align: center; margin-top: -20px; }
    .sub-title { text-align: center; color: #666666; font-size: 16px; margin-bottom: 20px; }
    
    /* Metric Card Styling - White Background with soft shadow */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Sidebar styling for light mode */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Scalable AI-Driven BI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enterprise Decision-Support & Market Insights System</div>', unsafe_allow_html=True)

# --- SIDEBAR: SYSTEM CONTROLS ---
with st.sidebar:
    st.header("⚙️ System Admin")
    
    # File Uploader
    raw_file = st.file_uploader("Upload Business Data (CSV)", type=["csv"])
    
    st.divider()
    st.subheader("Display Settings")
    full_view_mode = st.checkbox("Show All Products in Tables", value=False)
    
    st.divider()
    st.subheader("Chart Scalability")
    chart_cap = st.slider("Max Visual Points", min_value=10, max_value=200, value=50)
    
    st.divider()
    st.info("Developed by Anas K A | B.E. Computer Science")

# --- DATA ORCHESTRATION (The "Auto-Load" Logic) ---
LOCAL_DATA_PATH = os.path.join("data", "ecommerce_10000_products.csv")

@st.cache_data
def fetch_and_cache_data(source):
    return load_data(source)

business_df = None

if raw_file is not None:
    business_df = fetch_and_cache_data(raw_file)
    st.sidebar.success("✅ Using: Uploaded Dataset")
elif os.path.exists(LOCAL_DATA_PATH):
    business_df = fetch_and_cache_data(LOCAL_DATA_PATH)
    st.sidebar.info("📂 Auto-loaded: Sample Inventory Data")
else:
    st.info("👋 Welcome! Please upload a business dataset in the sidebar to begin analysis.")
    st.stop()

# --- MAIN APPLICATION LOGIC ---
if business_df is not None:
    schema_errors = validate_data_schema(business_df)
    if schema_errors:
        st.error(f"Schema Validation Failed. Missing columns: {schema_errors}")
        st.stop()

    view_limit = len(business_df) if full_view_mode else 5

    # SECTION 1: EXECUTIVE KPI SUMMARY
    metrics = calculate_kpi_metrics(business_df)
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric("📦 Total Products", f"{metrics['Total Products']:,}")
    m2.metric("💰 Total Sales Units", f"{metrics['Total Sales']:,}")
    m3.metric("💵 Total Revenue", f"₹{metrics['Total Revenue (₹)']:,.0f}")
    m4.metric("⭐ Avg Rating", f"{metrics['Average Rating']}/5")

    st.divider()

    # SECTION 2: ANALYTICS ENGINE
    analytics_tabs = st.tabs(["🏆 Performance Rankings", "📈 Market Visualizer", "💡 AI Recommendation"])

    # TAB 1: RANKINGS & PERFORMANCE
    with analytics_tabs[0]:
        left_col, right_col = st.columns(2)
        with left_col:
            st.subheader("High-Volume Leaders")
            st.dataframe(get_market_leaders(business_df, top_n=view_limit), use_container_width=True, hide_index=True)
            
        with right_col:
            st.subheader("Balanced Performance Analysis")
            st.dataframe(get_performance_ranking(business_df, top_n=view_limit), use_container_width=True, hide_index=True)

    # TAB 2: MARKET VISUALIZER
    with analytics_tabs[1]:
        st.subheader("Market Insight Analytics")
        product_query = st.text_input("🔍 Search for any product:", placeholder="Type product name here...")

        if product_query:
            search_results = business_df[business_df['name'].str.contains(product_query, case=False)]
            if not search_results.empty:
                st.success(f"Displaying {len(search_results)} result(s) found in the dataset.")
                fig = px.scatter(
                    search_results, x="price", y="sales", size="rating", color="rating",
                    hover_name="name", template="plotly_white", color_continuous_scale="Turbo"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"No results found for '{product_query}'.")
        else:
            st.info(f"Showing Top {chart_cap} Market Leaders by Sales")
            top_snapshot = business_df.nlargest(chart_cap, 'sales')
            fig = px.scatter(
                top_snapshot, x="price", y="sales", size="rating", color="rating",
                hover_name="name", template="plotly_white", color_continuous_scale="Viridis",
                opacity=0.7
            )
            st.plotly_chart(fig, use_container_width=True)

    # TAB 3: SMART RECOMMENDATION ENGINE
    with analytics_tabs[2]:
        st.subheader("AI Recommendation Engine")
        budget_input = st.number_input("Enter Target Budget (₹)", min_value=0, value=5000, step=500)
        
        if st.button("Generate Recommendations"):
            recommendations = run_recommendation_engine(business_df, budget_input)
            
            if recommendations.empty:
                st.warning("No products found within the specified budget.")
            else:
                st.success(f"Found {len(recommendations)} optimized suggestions within ₹{budget_input:,}")
                st.dataframe(recommendations, use_container_width=True, hide_index=True)
                
                export_data = recommendations.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download AI Report", export_data, "ai_recommendation_report.csv", "text/csv")