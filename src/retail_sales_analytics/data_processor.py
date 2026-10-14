import logging
from pathlib import Path
from typing import List, Optional, Union
import numpy as np
import pandas as pd

from .config import (
    HIGH_VALUE_THRESHOLD,
    CORE_TARGET_CITIES,
    PROCESSED_DATASET_CSV,
    PROCESSED_DATASET_EXCEL,
)

logger = logging.getLogger(__name__)


def clean_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw DataFrame:
    - Creates a copy to prevent mutation
    - Standardizes column names
    - Converts Date column to datetime
    - Coerces numeric columns
    - Strips whitespace from string columns
    """
    df = df.copy()

    # Strip column names
    df.columns = [c.strip() for c in df.columns]

    # Convert Date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Numeric columns
    numeric_cols = ["Unit_Price", "Quantity", "Total_Revenue", "Cost_Price"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Text columns strip
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    return df


def engineer_features(
    df: pd.DataFrame, high_value_threshold: float = HIGH_VALUE_THRESHOLD
) -> pd.DataFrame:
    """
    Engineers business intelligence metrics and time features:
    - Net_Profit: Total_Revenue - Cost_Price
    - Profit_Margin_Pct: (Net_Profit / Total_Revenue) * 100
    - Order_Label: 'High Value' if Total_Revenue > threshold else 'Standard'
    - Date features: Year, Month, Month_Name, Day_Name
    """
    df = df.copy()

    # Net Profit & Profit Margin
    df["Net_Profit"] = df["Total_Revenue"] - df["Cost_Price"]

    # Safe division for Profit Margin Percentage
    df["Profit_Margin_Pct"] = np.where(
        df["Total_Revenue"] != 0,
        (df["Net_Profit"] / df["Total_Revenue"]) * 100.0,
        0.0,
    )
    df["Profit_Margin_Pct"] = df["Profit_Margin_Pct"].round(2)

    # Order Value Categorization
    df["Order_Label"] = np.where(
        df["Total_Revenue"] > high_value_threshold,
        "High Value",
        "Standard",
    )

    # Date temporal features if Date exists
    if "Date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        df["Month_Name"] = df["Date"].dt.strftime("%b")
        df["Day_Name"] = df["Date"].dt.strftime("%A")

    return df


def get_category_subset(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """Extract rows matching a specific product category."""
    return df[df["Category"].str.lower() == category.lower()].copy()


def get_bulk_orders_by_payment(
    df: pd.DataFrame, min_quantity: int = 5, payment_method: str = "UPI"
) -> pd.DataFrame:
    """Extract orders with quantity >= min_quantity and specific payment method."""
    condition = (df["Quantity"] >= min_quantity) & (
        df["Payment_Method"].str.lower() == payment_method.lower()
    )
    return df[condition].copy()


def get_city_subset(
    df: pd.DataFrame, cities: Optional[List[str]] = None
) -> pd.DataFrame:
    """Extract orders originating from designated target cities."""
    target_cities = cities if cities is not None else CORE_TARGET_CITIES
    return df[df["Store_City"].isin(target_cities)].copy()


def get_orders_outside_city(df: pd.DataFrame, exclude_city: str = "Chennai") -> pd.DataFrame:
    """Extract orders from all locations excluding the designated city."""
    return df[df["Store_City"].str.lower() != exclude_city.lower()].copy()


def process_pipeline(
    df: pd.DataFrame,
    save_outputs: bool = True,
    csv_path: Optional[Union[str, Path]] = None,
    excel_path: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """
    Executes the entire data cleaning and feature engineering pipeline.
    Optionally saves the processed data to disk.
    """
    logger.info("Executing cleaning and feature engineering pipeline...")
    cleaned = clean_and_prepare(df)
    processed = engineer_features(cleaned)

    if save_outputs:
        target_csv = Path(csv_path) if csv_path else PROCESSED_DATASET_CSV
        target_excel = Path(excel_path) if excel_path else PROCESSED_DATASET_EXCEL

        target_csv.parent.mkdir(parents=True, exist_ok=True)
        processed.to_csv(target_csv, index=False)
        logger.info(f"Saved processed dataset to CSV: {target_csv}")

        try:
            processed.to_excel(target_excel, index=False)
            logger.info(f"Saved processed dataset to Excel: {target_excel}")
        except Exception as e:
            logger.warning(f"Could not save to Excel: {e}")

    return processed
