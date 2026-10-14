from dataclasses import dataclass
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd


@dataclass
class RevenueVectorMetrics:
    total_sum: float
    mean: float
    median: float
    std_dev: float
    variance: float
    min_val: float
    max_val: float
    total_count: int
    dtype: str


class RetailAnalytics:
    """
    Core analytics and metrics engine for retail sales performance.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def compute_revenue_vector_metrics(self) -> Tuple[RevenueVectorMetrics, np.ndarray]:
        """
        Computes NumPy 1D array statistical operations and cumulative sum.
        """
        revenue_array = np.array(self.df["Total_Revenue"])
        metrics = RevenueVectorMetrics(
            total_sum=float(np.sum(revenue_array)),
            mean=float(np.mean(revenue_array)),
            median=float(np.median(revenue_array)),
            std_dev=float(np.std(revenue_array)),
            variance=float(np.var(revenue_array)),
            min_val=float(np.min(revenue_array)),
            max_val=float(np.max(revenue_array)),
            total_count=int(len(revenue_array)),
            dtype=str(revenue_array.dtype),
        )
        cumulative_revenue = np.cumsum(revenue_array)
        return metrics, cumulative_revenue

    def compute_twodim_pricing_matrix(self) -> np.ndarray:
        """
        Constructs and returns the 2D NumPy array: [Unit_Price, Quantity].
        """
        return np.array([self.df["Unit_Price"].values, self.df["Quantity"].values])

    def get_numeric_summary(self) -> pd.DataFrame:
        """
        Returns descriptive statistics table for all numeric features.
        """
        num_df = self.df.select_dtypes(include="number")
        summary = pd.DataFrame(
            {
                "Count": num_df.count(),
                "Min": num_df.min(),
                "Max": num_df.max(),
                "Mean": num_df.mean().round(2),
                "Median": num_df.median().round(2),
                "Std": num_df.std().round(2),
            }
        )
        return summary

    def get_category_summary(self) -> pd.DataFrame:
        """
        Aggregates performance by Category:
        - Total Revenue
        - Average Revenue
        - Number of Sales
        - Total Net Profit
        - Average Profit Margin %
        """
        summary = (
            self.df.groupby("Category")
            .agg(
                Total_Revenue=("Total_Revenue", "sum"),
                Average_Revenue=("Total_Revenue", "mean"),
                Number_of_Sales=("Total_Revenue", "count"),
                Total_Net_Profit=("Net_Profit", "sum"),
                Avg_Profit_Margin_Pct=("Profit_Margin_Pct", "mean"),
            )
            .reset_index()
        )
        summary["Average_Revenue"] = summary["Average_Revenue"].round(2)
        summary["Avg_Profit_Margin_Pct"] = summary["Avg_Profit_Margin_Pct"].round(2)
        return summary.sort_values(by="Total_Revenue", ascending=False)

    def get_city_summary(self) -> pd.DataFrame:
        """
        Aggregates performance by Store City.
        """
        summary = (
            self.df.groupby("Store_City")
            .agg(
                Total_Revenue=("Total_Revenue", "sum"),
                Total_Net_Profit=("Net_Profit", "sum"),
                Total_Orders=("Transaction_ID", "count"),
                Average_Order_Value=("Total_Revenue", "mean"),
            )
            .reset_index()
        )
        summary["Average_Order_Value"] = summary["Average_Order_Value"].round(2)
        return summary.sort_values(by="Total_Revenue", ascending=False)

    def get_payment_method_summary(self) -> pd.DataFrame:
        """
        Aggregates performance and profitability by Payment Method.
        """
        summary = (
            self.df.groupby("Payment_Method")
            .agg(
                Average_Net_Profit=("Net_Profit", "mean"),
                Total_Net_Profit=("Net_Profit", "sum"),
                Total_Revenue=("Total_Revenue", "sum"),
                Transaction_Count=("Transaction_ID", "count"),
            )
            .reset_index()
        )
        summary["Average_Net_Profit"] = summary["Average_Net_Profit"].round(2)
        return summary.sort_values(by="Average_Net_Profit", ascending=False)

    def get_daily_sales_series(self) -> pd.Series:
        """
        Returns time series of daily revenue aggregated by Date.
        """
        return self.df.groupby("Date")["Total_Revenue"].sum().sort_index()

    def get_extreme_transactions(self) -> Dict[str, Any]:
        """
        Identifies the highest and lowest revenue transactions.
        """
        best_idx = self.df["Total_Revenue"].idxmax()
        worst_idx = self.df["Total_Revenue"].idxmin()

        best_row = self.df.loc[best_idx].to_dict()
        worst_row = self.df.loc[worst_idx].to_dict()

        return {
            "highest_revenue_order": {
                "index": int(best_idx),
                "transaction_id": best_row.get("Transaction_ID"),
                "product_name": best_row.get("Product_Name"),
                "category": best_row.get("Category"),
                "store_city": best_row.get("Store_City"),
                "revenue": float(best_row.get("Total_Revenue")),
                "net_profit": float(best_row.get("Net_Profit")),
            },
            "lowest_revenue_order": {
                "index": int(worst_idx),
                "transaction_id": worst_row.get("Transaction_ID"),
                "product_name": worst_row.get("Product_Name"),
                "category": worst_row.get("Category"),
                "store_city": worst_row.get("Store_City"),
                "revenue": float(worst_row.get("Total_Revenue")),
                "net_profit": float(worst_row.get("Net_Profit")),
            },
        }

    def get_kpi_summary(self) -> Dict[str, Any]:
        """
        Calculates high-level executive KPIs.
        """
        total_revenue = float(self.df["Total_Revenue"].sum())
        total_profit = float(self.df["Net_Profit"].sum())
        overall_margin = (
            (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0
        )
        high_value_orders = int((self.df["Order_Label"] == "High Value").sum())
        total_orders = len(self.df)

        return {
            "total_transactions": total_orders,
            "unique_categories": int(self.df["Category"].nunique()),
            "unique_products": int(self.df["Product_Name"].nunique()),
            "unique_cities": int(self.df["Store_City"].nunique()),
            "total_revenue": total_revenue,
            "total_net_profit": total_profit,
            "overall_profit_margin_pct": round(overall_margin, 2),
            "average_order_value": round(float(self.df["Total_Revenue"].mean()), 2),
            "high_value_orders_count": high_value_orders,
            "high_value_orders_pct": round((high_value_orders / total_orders) * 100, 2),
        }
