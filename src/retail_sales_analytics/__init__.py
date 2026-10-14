"""
Retail Sales Analytics & Business Intelligence Package

A modular, production-ready framework for retail data analytics,
feature engineering, business intelligence KPIs, and visualization.
"""

from .analytics import RetailAnalytics, RevenueVectorMetrics
from .config import (
    HIGH_VALUE_THRESHOLD,
    CORE_TARGET_CITIES,
    LOCAL_DATASET_PATH,
    PROCESSED_DATASET_CSV,
    PROCESSED_DATASET_EXCEL,
    REPORTS_DIR,
    FIGURES_DIR,
)
from .data_loader import load_data, validate_schema
from .data_processor import (
    clean_and_prepare,
    engineer_features,
    get_bulk_orders_by_payment,
    get_category_subset,
    get_city_subset,
    get_orders_outside_city,
    process_pipeline,
)
from .reporter import ReportGenerator
from .visualizer import RetailVisualizer

__version__ = "1.0.0"

__all__ = [
    "load_data",
    "validate_schema",
    "clean_and_prepare",
    "engineer_features",
    "process_pipeline",
    "get_category_subset",
    "get_bulk_orders_by_payment",
    "get_city_subset",
    "get_orders_outside_city",
    "RetailAnalytics",
    "RevenueVectorMetrics",
    "RetailVisualizer",
    "ReportGenerator",
    "HIGH_VALUE_THRESHOLD",
    "CORE_TARGET_CITIES",
    "LOCAL_DATASET_PATH",
    "PROCESSED_DATASET_CSV",
    "PROCESSED_DATASET_EXCEL",
    "REPORTS_DIR",
    "FIGURES_DIR",
]
