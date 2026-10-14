import pandas as pd
import pytest

from retail_sales_analytics import (
    clean_and_prepare,
    engineer_features,
    get_category_subset,
    get_bulk_orders_by_payment,
    get_city_subset,
    get_orders_outside_city,
)


@pytest.fixture
def sample_raw_dataframe():
    data = {
        "Transaction_ID": ["T1", "T2", "T3"],
        "Date": ["2025-01-01", "2025-02-15", "2025-03-20"],
        "Product_ID": ["P1", "P2", "P3"],
        "Product_Name": [" Keyboard ", "Pen ", "Stand"],
        "Category": ["Electronics", "Stationery", "Accessories"],
        "Unit_Price": [2000, 50, 1500],
        "Quantity": [3, 10, 4],
        "Total_Revenue": [6000, 500, 6000],
        "Cost_Price": [4000, 200, 3600],
        "Payment_Method": ["UPI", "UPI", "Credit Card"],
        "Store_City": ["Chennai", "Madurai", "Coimbatore"],
    }
    return pd.DataFrame(data)


def test_clean_and_prepare(sample_raw_dataframe):
    cleaned = clean_and_prepare(sample_raw_dataframe)
    assert pd.api.types.is_datetime64_any_dtype(cleaned["Date"])
    assert cleaned.loc[0, "Product_Name"] == "Keyboard"
    assert cleaned.loc[1, "Product_Name"] == "Pen"


def test_engineer_features(sample_raw_dataframe):
    cleaned = clean_and_prepare(sample_raw_dataframe)
    processed = engineer_features(cleaned, high_value_threshold=5000.0)

    # Net Profit
    assert processed.loc[0, "Net_Profit"] == 2000  # 6000 - 4000
    assert processed.loc[1, "Net_Profit"] == 300   # 500 - 200

    # Profit Margin Pct
    assert processed.loc[0, "Profit_Margin_Pct"] == pytest.approx(33.33, 0.01)
    assert processed.loc[1, "Profit_Margin_Pct"] == pytest.approx(60.0, 0.01)

    # Order Label
    assert processed.loc[0, "Order_Label"] == "High Value"
    assert processed.loc[1, "Order_Label"] == "Standard"
    assert processed.loc[2, "Order_Label"] == "High Value"

    # Temporal features
    assert processed.loc[0, "Year"] == 2025
    assert processed.loc[0, "Month"] == 1


def test_subsets_and_filters(sample_raw_dataframe):
    cleaned = clean_and_prepare(sample_raw_dataframe)
    processed = engineer_features(cleaned)

    # Category subset
    elec = get_category_subset(processed, "Electronics")
    assert len(elec) == 1
    assert elec.iloc[0]["Product_ID"] == "P1"

    # Bulk UPI orders (Qty >= 5 and Payment == UPI)
    bulk_upi = get_bulk_orders_by_payment(processed, min_quantity=5, payment_method="UPI")
    assert len(bulk_upi) == 1
    assert bulk_upi.iloc[0]["Transaction_ID"] == "T2"

    # City filter
    target_cities = get_city_subset(processed, ["Chennai", "Madurai"])
    assert len(target_cities) == 2

    # Outside Chennai filter
    outside_chennai = get_orders_outside_city(processed, "Chennai")
    assert len(outside_chennai) == 2
    assert "Chennai" not in outside_chennai["Store_City"].values
