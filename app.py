import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# Add project root to sys.path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from retail_sales_analytics import (
    load_data,
    process_pipeline,
    RetailAnalytics,
    RetailVisualizer,
)

# Page configuration
st.set_page_config(
    page_title="Retail Sales Analytics & Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 28px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 20px;
    }
    [data-testid="stMetricValue"] {
        font-size: 26px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_default_dataset():
    raw_df = load_data()
    return process_pipeline(raw_df, save_outputs=False)


# Sidebar Header & Controls
st.sidebar.title("🛒 Sales Analytics")
st.sidebar.caption("Retail Performance Dashboard")

# File Uploader in Sidebar
uploaded_file = st.sidebar.file_uploader(
    "Upload custom dataset (.xlsx / .csv)", type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:
    try:
        suffix = Path(uploaded_file.name).suffix.lower()
        if suffix in [".xlsx", ".xls"]:
            raw_data = pd.read_excel(uploaded_file)
        else:
            raw_data = pd.read_csv(uploaded_file)
        df = process_pipeline(raw_data, save_outputs=False)
        st.sidebar.success(f"Loaded custom file: {uploaded_file.name}")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
        df = load_default_dataset()
else:
    df = load_default_dataset()

# Sidebar Filters
st.sidebar.subheader("Filter Data")

# Category filter
all_categories = sorted(df["Category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Product Category", options=all_categories, default=all_categories
)

# City filter
all_cities = sorted(df["Store_City"].unique().tolist())
selected_cities = st.sidebar.multiselect(
    "Store City", options=all_cities, default=all_cities
)

# Payment method filter
all_payments = sorted(df["Payment_Method"].unique().tolist())
selected_payments = st.sidebar.multiselect(
    "Payment Gateway", options=all_payments, default=all_payments
)

# Segment filter
all_segments = ["All", "High Value", "Standard"]
selected_segment = st.sidebar.selectbox("Order Segment", options=all_segments)

# Apply filters
filtered_df = df.copy()

if selected_categories:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
if selected_cities:
    filtered_df = filtered_df[filtered_df["Store_City"].isin(selected_cities)]
if selected_payments:
    filtered_df = filtered_df[filtered_df["Payment_Method"].isin(selected_payments)]
if selected_segment != "All":
    filtered_df = filtered_df[filtered_df["Order_Label"] == selected_segment]

# Analytics instance on filtered data
analytics = RetailAnalytics(filtered_df)
kpis = analytics.get_kpi_summary()

# Main Title
st.markdown('<div class="main-header">Retail Sales Analytics & Business Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Executive Performance Dashboard & Insights Engine</div>', unsafe_allow_html=True)

# Top KPIs Row
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Gross Revenue", f"₹{kpis['total_revenue']:,.0f}")
kpi2.metric("Net Profit", f"₹{kpis['total_net_profit']:,.0f}", f"{kpis['overall_profit_margin_pct']}% margin")
kpi3.metric("Average Order Value", f"₹{kpis['average_order_value']:,.0f}")
kpi4.metric("Orders Analyzed", f"{kpis['total_transactions']:,}")
kpi5.metric("High-Value Orders", f"{kpis['high_value_orders_count']}", f"{kpis['high_value_orders_pct']}% of total")

st.divider()

# Tabs
tab_overview, tab_explorer, tab_insights = st.tabs(["📊 Performance Visuals", "📋 Data Explorer", "📈 Deep Insights"])

visualizer = RetailVisualizer(filtered_df)

with tab_overview:
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Daily Sales Revenue Timeline")
        daily_sales = filtered_df.groupby("Date")["Total_Revenue"].sum().sort_index()
        st.line_chart(daily_sales)

    with col_right:
        st.subheader("Revenue by Category")
        cat_rev = filtered_df.groupby("Category")["Total_Revenue"].sum()
        st.bar_chart(cat_rev)

    col_city, col_pay = st.columns(2)
    with col_city:
        st.subheader("Total Revenue by Store City")
        city_rev = filtered_df.groupby("Store_City")["Total_Revenue"].sum().sort_values(ascending=False)
        st.bar_chart(city_rev)

    with col_pay:
        st.subheader("Average Profit by Payment Method")
        pay_profit = filtered_df.groupby("Payment_Method")["Net_Profit"].mean().sort_values(ascending=False)
        st.bar_chart(pay_profit)

with tab_explorer:
    st.subheader(f"Transaction Records ({len(filtered_df):,} orders)")

    display_cols = [
        "Transaction_ID",
        "Date",
        "Product_Name",
        "Category",
        "Unit_Price",
        "Quantity",
        "Total_Revenue",
        "Net_Profit",
        "Profit_Margin_Pct",
        "Order_Label",
        "Payment_Method",
        "Store_City",
    ]

    st.dataframe(
        filtered_df[display_cols].sort_values(by="Date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    # Download CSV
    csv_bytes = filtered_df[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="retail_sales_filtered.csv",
        mime="text/csv",
    )

with tab_insights:
    st.subheader("Category Breakdown")
    st.dataframe(analytics.get_category_summary(), use_container_width=True, hide_index=True)

    st.subheader("City Breakdown")
    st.dataframe(analytics.get_city_summary(), use_container_width=True, hide_index=True)

    st.subheader("Outlier Transactions")
    extremes = analytics.get_extreme_transactions()
    high = extremes["highest_revenue_order"]
    low = extremes["lowest_revenue_order"]

    col_high, col_low = st.columns(2)
    with col_high:
        st.info(
            f"**Highest Revenue Order:** #{high['transaction_id']}\n\n"
            f"- Product: **{high['product_name']}** ({high['category']})\n"
            f"- City: **{high['store_city']}**\n"
            f"- Revenue: **₹{high['revenue']:,.2f}** | Profit: **₹{high['net_profit']:,.2f}**"
        )
    with col_low:
        st.warning(
            f"**Lowest Revenue Order:** #{low['transaction_id']}\n\n"
            f"- Product: **{low['product_name']}** ({low['category']})\n"
            f"- City: **{low['store_city']}**\n"
            f"- Revenue: **₹{low['revenue']:,.2f}** | Profit: **₹{low['net_profit']:,.2f}**"
        )
