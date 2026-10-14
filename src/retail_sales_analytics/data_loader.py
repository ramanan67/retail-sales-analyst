import logging
from pathlib import Path
from typing import Optional, Union
import pandas as pd

from .config import LOCAL_DATASET_PATH, EXTERNAL_DATASET_PATH

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "Transaction_ID",
    "Date",
    "Product_ID",
    "Product_Name",
    "Category",
    "Unit_Price",
    "Quantity",
    "Total_Revenue",
    "Cost_Price",
    "Payment_Method",
    "Store_City",
]


def resolve_data_path(filepath: Optional[Union[str, Path]] = None) -> Path:
    """
    Resolve the path to the dataset file using fallbacks.
    """
    if filepath is not None:
        path = Path(filepath)
        if path.exists():
            return path
        raise FileNotFoundError(f"Provided dataset file not found at: {path}")

    if LOCAL_DATASET_PATH.exists():
        return LOCAL_DATASET_PATH

    if EXTERNAL_DATASET_PATH.exists():
        return EXTERNAL_DATASET_PATH

    raise FileNotFoundError(
        f"Dataset not found. Checked default local path ({LOCAL_DATASET_PATH}) "
        f"and external path ({EXTERNAL_DATASET_PATH}). "
        f"Please supply a valid path to Retail_Sales_Easy_Project.xlsx"
    )


def validate_schema(df: pd.DataFrame) -> bool:
    """
    Validate that all required columns are present in the dataframe.
    """
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")
    return True


def load_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Load retail sales dataset from Excel or CSV file.
    """
    target_path = resolve_data_path(filepath)
    logger.info(f"Loading data from: {target_path}")

    suffix = target_path.suffix.lower()
    if suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(target_path)
    elif suffix == ".csv":
        df = pd.read_csv(target_path)
    else:
        raise ValueError(f"Unsupported file format '{suffix}'. Supported: .xlsx, .xls, .csv")

    validate_schema(df)
    logger.info(f"Data successfully loaded. Shape: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df
