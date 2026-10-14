import logging
from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd

from .config import FIGURES_DIR, DEFAULT_DPI

logger = logging.getLogger(__name__)


class RetailVisualizer:
    """
    Generates publication-quality visualizations for retail analytics.
    """

    def __init__(self, df: pd.DataFrame, output_dir: Optional[Path] = None):
        self.df = df
        self.output_dir = output_dir or FIGURES_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_theme(style="whitegrid")
        plt.rcParams["font.sans-serif"] = "Arial"
        plt.rcParams["font.family"] = "sans-serif"

    def plot_daily_sales_trend(
        self,
        filename: str = "01_daily_revenue_trend.png",
        show: bool = False,
    ) -> Path:
        """
        Plots daily sales revenue trend with optional rolling average.
        """
        daily_sales = (
            self.df.groupby("Date")["Total_Revenue"].sum().sort_index()
        )

        fig, ax = plt.subplots(figsize=(13, 5), dpi=DEFAULT_DPI)
        ax.plot(
            daily_sales.index,
            daily_sales.values,
            marker="o",
            markersize=3,
            color="#2b5c8f",
            linewidth=1.5,
            label="Daily Revenue",
            alpha=0.85,
        )

        # 7-day rolling average for smoother trend line
        if len(daily_sales) >= 7:
            rolling_7d = daily_sales.rolling(window=7, min_periods=1).mean()
            ax.plot(
                rolling_7d.index,
                rolling_7d.values,
                color="#e74c3c",
                linewidth=2.5,
                linestyle="--",
                label="7-Day Moving Average",
            )

        ax.set_title("Daily Sales Revenue Trend (Jan - Jun 2025)", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Date", fontsize=11, fontweight="bold")
        ax.set_ylabel("Revenue (INR ₹)", fontsize=11, fontweight="bold")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.yaxis.set_major_formatter("₹{:,.0f}".format)
        plt.xticks(rotation=45)
        ax.legend(frameon=True, facecolor="white", loc="upper right")
        plt.tight_layout()

        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=DEFAULT_DPI)
        logger.info(f"Saved figure: {filepath}")
        if show:
            plt.show()
        plt.close(fig)
        return filepath

    def plot_city_revenue(
        self,
        filename: str = "02_city_revenue_comparison.png",
        show: bool = False,
    ) -> Path:
        """
        Plots total revenue by store city with data value labels.
        """
        city_rev = (
            self.df.groupby("Store_City")["Total_Revenue"].sum().sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(10, 5), dpi=DEFAULT_DPI)
        colors = sns.color_palette("mako", len(city_rev))
        bars = ax.bar(city_rev.index, city_rev.values, color=colors, edgecolor="black", linewidth=0.6, width=0.55)

        # Add data labels
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"₹{height:,.0f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9.5,
                fontweight="bold",
            )

        ax.set_title("Total Sales Revenue by City", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("City", fontsize=11, fontweight="bold")
        ax.set_ylabel("Total Revenue (INR ₹)", fontsize=11, fontweight="bold")
        ax.yaxis.set_major_formatter("₹{:,.0f}".format)
        ax.set_ylim(0, city_rev.max() * 1.15)
        plt.tight_layout()

        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=DEFAULT_DPI)
        logger.info(f"Saved figure: {filepath}")
        if show:
            plt.show()
        plt.close(fig)
        return filepath

    def plot_category_distribution(
        self,
        filename: str = "03_category_revenue_pie.png",
        show: bool = False,
    ) -> Path:
        """
        Plots revenue share by product category as an elegant donut chart.
        (Fixes the mislabeled title in the original script).
        """
        cat_rev = self.df.groupby("Category")["Total_Revenue"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(7, 7), dpi=DEFAULT_DPI)
        colors = ["#3498db", "#2ecc71", "#f39c12"]
        wedges, texts, autotexts = ax.pie(
            cat_rev.values,
            labels=cat_rev.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors[: len(cat_rev)],
            explode=[0.04] * len(cat_rev),
            wedgeprops={"edgecolor": "white", "linewidth": 2, "antialiased": True},
            textprops={"fontsize": 11, "fontweight": "bold"},
        )

        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(11)

        # Draw circle for donut style
        centre_circle = plt.Circle((0, 0), 0.65, fc="white")
        fig.gca().add_artist(centre_circle)

        total_rev = cat_rev.sum()
        ax.text(
            0,
            0,
            f"Total Revenue\n₹{total_rev:,.0f}",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=11,
            fontweight="bold",
            color="#2c3e50",
        )

        ax.set_title("Revenue Contribution by Category", fontsize=14, fontweight="bold", pad=15)
        plt.tight_layout()

        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=DEFAULT_DPI)
        logger.info(f"Saved figure: {filepath}")
        if show:
            plt.show()
        plt.close(fig)
        return filepath

    def plot_unit_price_vs_quantity(
        self,
        filename: str = "04_unit_price_vs_quantity_scatter.png",
        show: bool = False,
    ) -> Path:
        """
        Scatter plot of Unit Price vs Quantity segmented by Category.
        """
        fig, ax = plt.subplots(figsize=(9, 6), dpi=DEFAULT_DPI)
        sns.scatterplot(
            data=self.df,
            x="Unit_Price",
            y="Quantity",
            hue="Category",
            style="Category",
            marker="d",
            s=120,
            alpha=0.85,
            edgecolor="black",
            linewidth=0.8,
            palette="deep",
            ax=ax,
        )

        ax.set_title("Unit Price vs. Quantity by Category", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Unit Price (INR ₹)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Quantity Purchased", fontsize=11, fontweight="bold")
        ax.xaxis.set_major_formatter("₹{:,.0f}".format)
        ax.legend(title="Product Category", title_fontsize="11", frameon=True, loc="upper right")
        plt.tight_layout()

        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=DEFAULT_DPI)
        logger.info(f"Saved figure: {filepath}")
        if show:
            plt.show()
        plt.close(fig)
        return filepath

    def plot_payment_profitability(
        self,
        filename: str = "05_payment_profitability.png",
        show: bool = False,
    ) -> Path:
        """
        Plots average net profit by payment method with annotations.
        """
        pay_profit = (
            self.df.groupby("Payment_Method")["Net_Profit"].mean().sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(9, 5), dpi=DEFAULT_DPI)
        colors = sns.color_palette("crest", len(pay_profit))
        bars = ax.bar(
            pay_profit.index,
            pay_profit.values,
            color=colors,
            edgecolor="black",
            linewidth=0.6,
            width=0.5,
        )

        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"₹{height:,.2f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

        ax.set_title("Average Net Profit by Payment Method", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Payment Method", fontsize=11, fontweight="bold")
        ax.set_ylabel("Average Net Profit (INR ₹)", fontsize=11, fontweight="bold")
        ax.yaxis.set_major_formatter("₹{:,.0f}".format)
        ax.set_ylim(0, pay_profit.max() * 1.15)
        plt.tight_layout()

        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=DEFAULT_DPI)
        logger.info(f"Saved figure: {filepath}")
        if show:
            plt.show()
        plt.close(fig)
        return filepath

    def generate_all_charts(self, show: bool = False) -> Dict[str, Path]:
        """
        Generates and saves all project charts.
        """
        return {
            "daily_trend": self.plot_daily_sales_trend(show=show),
            "city_revenue": self.plot_city_revenue(show=show),
            "category_distribution": self.plot_category_distribution(show=show),
            "price_vs_quantity": self.plot_unit_price_vs_quantity(show=show),
            "payment_profit": self.plot_payment_profitability(show=show),
        }
