import argparse
import sys
from pathlib import Path
from typing import Optional

from .analytics import RetailAnalytics
from .data_loader import load_data
from .data_processor import (
    get_bulk_orders_by_payment,
    get_category_subset,
    get_city_subset,
    get_orders_outside_city,
    process_pipeline,
)
from .reporter import ReportGenerator
from .visualizer import RetailVisualizer


def _setup_windows_encoding():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def print_section(title: str):
    print("\n" + "=" * 75)
    print(f"  {title.upper()}")
    print("=" * 75)


def run_pipeline(
    data_path: Optional[str] = None,
    show_plots: bool = False,
    save_outputs: bool = True,
):
    _setup_windows_encoding()

    print_section("1. Data Ingestion & Health Check")
    raw_df = load_data(data_path)
    print("✓ Dataset loaded successfully.")
    print(f"✓ Dimensions: {raw_df.shape[0]} rows x {raw_df.shape[1]} columns")
    print(f"✓ Missing Values:\n{raw_df.isnull().sum().to_string()}")

    print_section("2. Data Processing & Feature Engineering")
    df = process_pipeline(raw_df, save_outputs=save_outputs)
    print("✓ Derived Features: Net_Profit, Profit_Margin_Pct, Order_Label")
    print("\nSample Processed Records (First 5):")
    print(
        df[
            [
                "Transaction_ID",
                "Product_Name",
                "Category",
                "Quantity",
                "Total_Revenue",
                "Net_Profit",
                "Profit_Margin_Pct",
                "Order_Label",
            ]
        ]
        .head(5)
        .to_string(index=False)
    )

    print_section("3. NumPy Vector & Matrix Operations")
    analytics = RetailAnalytics(df)
    vec_metrics, cumsum = analytics.compute_revenue_vector_metrics()
    pricing_matrix = analytics.compute_twodim_pricing_matrix()

    print(f"Total Revenue Array Length: {vec_metrics.total_count}")
    print(f"Data Type: {vec_metrics.dtype}")
    print(f"Sum:           ₹{vec_metrics.total_sum:,.2f}")
    print(f"Mean:          ₹{vec_metrics.mean:,.2f}")
    print(f"Median:        ₹{vec_metrics.median:,.2f}")
    print(f"Std Dev:       ₹{vec_metrics.std_dev:,.2f}")
    print(f"Variance:      {vec_metrics.variance:,.2f}")
    print(f"Min:           ₹{vec_metrics.min_val:,.2f}")
    print(f"Max:           ₹{vec_metrics.max_val:,.2f}")
    print(f"Cumulative Sum (first 5 steps): {cumsum[:5]}")
    print(f"2D Matrix [Unit_Price, Quantity] Shape: {pricing_matrix.shape}")

    print_section("4. Specific Targeted Queries & Filters")
    print("\n[A] First 10 Records:")
    print(df[["Transaction_ID", "Product_Name", "Total_Revenue"]].head(10).to_string(index=False))

    print("\n[B] Sliced Records (Indices 100 to 110 - Sample):")
    print(df.loc[100:110, ["Product_Name", "Total_Revenue", "Store_City"]].to_string())

    electronics = get_category_subset(df, "Electronics")
    print(f"\n[C] Category 'Electronics': {len(electronics)} transactions.")

    upi_bulk = get_bulk_orders_by_payment(df, min_quantity=5, payment_method="UPI")
    print(f"\n[D] Bulk Orders (Qty >= 5 via UPI): {len(upi_bulk)} transactions.")

    core_cities = get_city_subset(df, ["Chennai", "Coimbatore", "Madurai"])
    print(f"\n[E] Orders in Core Cities (Chennai, Coimbatore, Madurai): {len(core_cities)} transactions.")

    outside_chennai = get_orders_outside_city(df, "Chennai")
    print(f"\n[F] Orders Outside Chennai: {len(outside_chennai)} transactions.")

    print_section("5. Aggregations & Business Insights")
    print("\nCategory Summary:")
    print(analytics.get_category_summary().to_string(index=False))

    print("\nCity Revenue Summary:")
    print(analytics.get_city_summary().to_string(index=False))

    print("\nPayment Method Profitability:")
    print(analytics.get_payment_method_summary().to_string(index=False))

    extremes = analytics.get_extreme_transactions()
    print("\nExtreme Orders:")
    best = extremes["highest_revenue_order"]
    worst = extremes["lowest_revenue_order"]
    print(f"Highest: Order #{best['transaction_id']} ({best['product_name']}) -> ₹{best['revenue']:,.2f} (Profit: ₹{best['net_profit']:,.2f})")
    print(f"Lowest:  Order #{worst['transaction_id']} ({worst['product_name']}) -> ₹{worst['revenue']:,.2f} (Profit: ₹{worst['net_profit']:,.2f})")

    print_section("6. Visualizations Generation")
    visualizer = RetailVisualizer(df)
    saved_charts = visualizer.generate_all_charts(show=show_plots)
    print("Generated publication-quality charts in 'reports/figures/':")
    for key, path in saved_charts.items():
        print(f"  ✓ {key.replace('_', ' ').title()}: {path.name}")

    if save_outputs:
        print_section("7. Executive Summary Report")
        reporter = ReportGenerator(analytics)
        report_path = reporter.save_report()
        print(f"✓ Executive report generated at: {report_path}")

    print("\n" + "=" * 75)
    print("  PROJECT EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 75 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Retail Sales Analytics & Business Intelligence Engine"
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default=None,
        help="Custom path to Retail_Sales_Easy_Project.xlsx or .csv",
    )
    parser.add_argument(
        "--show-plots",
        "-s",
        action="store_true",
        help="Display matplotlib/seaborn plots interactively in windows",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Disable automatic saving of processed data and reports",
    )

    args = parser.parse_args()
    run_pipeline(
        data_path=args.file,
        show_plots=args.show_plots,
        save_outputs=not args.no_save,
    )


if __name__ == "__main__":
    main()
