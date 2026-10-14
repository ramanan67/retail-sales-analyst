import numpy as np
import pandas as pd
import pytest

from retail_sales_analytics import RetailAnalytics


@pytest.fixture
def sample_processed_df():
    data = {
        "Transaction_ID": ["TRX-1", "TRX-2", "TRX-3", "TRX-4"],
        "Date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"]),
        "Product_ID": ["P1", "P2", "P3", "P4"],
        "Product_Name": ["Laptop Stand", "Keyboard", "Notebook", "Mouse"],
        "Category": ["Accessories", "Electronics", "Stationery", "Electronics"],
        "Unit_Price": [1000, 3000, 200, 1500],
        "Quantity": [2, 2, 5, 2],
        "Total_Revenue": [2000, 6000, 1000, 3000],
        "Cost_Price": [1200, 4000, 500, 2000],
        "Net_Profit": [800, 2000, 500, 1000],
        "Profit_Margin_Pct": [40.0, 33.33, 50.0, 33.33],
        "Order_Label": ["Standard", "High Value", "Standard", "Standard"],
        "Payment_Method": ["Cash", "UPI", "Credit Card", "Debit Card"],
        "Store_City": ["Chennai", "Coimbatore", "Chennai", "Madurai"],
    }
    return pd.DataFrame(data)


def test_revenue_vector_metrics(sample_processed_df):
    analytics = RetailAnalytics(sample_processed_df)
    metrics, cumsum = analytics.compute_revenue_vector_metrics()

    assert metrics.total_count == 4
    assert metrics.total_sum == 12000.0
    assert metrics.mean == 3000.0
    assert metrics.min_val == 1000.0
    assert metrics.max_val == 6000.0
    assert np.array_equal(cumsum, np.array([2000, 8000, 9000, 12000]))


def test_pricing_matrix(sample_processed_df):
    analytics = RetailAnalytics(sample_processed_df)
    matrix = analytics.compute_twodim_pricing_matrix()
    assert matrix.shape == (2, 4)
    # Unit prices row
    assert list(matrix[0]) == [1000, 3000, 200, 1500]
    # Quantities row
    assert list(matrix[1]) == [2, 2, 5, 2]


def test_category_summary(sample_processed_df):
    analytics = RetailAnalytics(sample_processed_df)
    cat_summary = analytics.get_category_summary()

    # Electronics should have 2 transactions, total revenue 9000
    elec_row = cat_summary[cat_summary["Category"] == "Electronics"].iloc[0]
    assert elec_row["Number_of_Sales"] == 2
    assert elec_row["Total_Revenue"] == 9000
    assert elec_row["Total_Net_Profit"] == 3000


def test_extreme_transactions(sample_processed_df):
    analytics = RetailAnalytics(sample_processed_df)
    extremes = analytics.get_extreme_transactions()

    assert extremes["highest_revenue_order"]["transaction_id"] == "TRX-2"
    assert extremes["highest_revenue_order"]["revenue"] == 6000.0
    assert extremes["lowest_revenue_order"]["transaction_id"] == "TRX-3"
    assert extremes["lowest_revenue_order"]["revenue"] == 1000.0


def test_kpi_summary(sample_processed_df):
    analytics = RetailAnalytics(sample_processed_df)
    kpis = analytics.get_kpi_summary()

    assert kpis["total_transactions"] == 4
    assert kpis["total_revenue"] == 12000.0
    assert kpis["total_net_profit"] == 4300.0
    assert kpis["high_value_orders_count"] == 1
    assert kpis["high_value_orders_pct"] == 25.0
