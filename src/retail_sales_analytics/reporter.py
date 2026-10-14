import logging
from pathlib import Path
from typing import Optional
import pandas as pd

from .config import EXECUTIVE_SUMMARY_REPORT
from .analytics import RetailAnalytics

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates structured executive markdown and text summary reports.
    """

    def __init__(self, analytics: RetailAnalytics, output_path: Optional[Path] = None):
        self.analytics = analytics
        self.output_path = output_path or EXECUTIVE_SUMMARY_REPORT

    def build_markdown_report(self) -> str:
        kpis = self.analytics.get_kpi_summary()
        cat_summary = self.analytics.get_category_summary()
        city_summary = self.analytics.get_city_summary()
        pay_summary = self.analytics.get_payment_method_summary()
        extremes = self.analytics.get_extreme_transactions()
        vec_metrics, _ = self.analytics.compute_revenue_vector_metrics()

        highest = extremes["highest_revenue_order"]
        lowest = extremes["lowest_revenue_order"]

        report = f"""# Executive Retail Sales Performance Report

## 1. Key Performance Indicators (KPIs)
| Metric | Value |
| :--- | :--- |
| **Total Transactions Analyzed** | {kpis['total_transactions']:,} |
| **Total Gross Revenue** | ₹{kpis['total_revenue']:,.2f} |
| **Total Net Profit** | ₹{kpis['total_net_profit']:,.2f} |
| **Overall Profit Margin** | {kpis['overall_profit_margin_pct']}% |
| **Average Order Value (AOV)** | ₹{kpis['average_order_value']:,.2f} |
| **High-Value Orders (> ₹5,000)** | {kpis['high_value_orders_count']} ({kpis['high_value_orders_pct']}%) |
| **Unique Product Lines** | {kpis['unique_products']} |
| **Store Locations (Cities)** | {kpis['unique_cities']} |

---

## 2. Statistical Distribution (Revenue Vector Analysis)
- **Vector Sum**: ₹{vec_metrics.total_sum:,.2f}
- **Mean Revenue**: ₹{vec_metrics.mean:,.2f}
- **Median Revenue**: ₹{vec_metrics.median:,.2f}
- **Standard Deviation**: ₹{vec_metrics.std_dev:,.2f}
- **Variance**: {vec_metrics.variance:,.2f}
- **Min / Max Revenue**: ₹{vec_metrics.min_val:,.2f} / ₹{vec_metrics.max_val:,.2f}

---

## 3. Product Category Breakdown
| Category | Total Revenue | Avg Revenue | Orders | Net Profit | Avg Margin % |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
        for _, row in cat_summary.iterrows():
            report += (
                f"| {row['Category']} | ₹{row['Total_Revenue']:,.2f} | "
                f"₹{row['Average_Revenue']:,.2f} | {int(row['Number_of_Sales'])} | "
                f"₹{row['Total_Net_Profit']:,.2f} | {row['Avg_Profit_Margin_Pct']}% |\n"
            )

        report += """
---

## 4. Geographic Performance by City
| City | Total Revenue | Net Profit | Total Orders | Average Order Value |
| :--- | :--- | :--- | :--- | :--- |
"""
        for _, row in city_summary.iterrows():
            report += (
                f"| {row['Store_City']} | ₹{row['Total_Revenue']:,.2f} | "
                f"₹{row['Total_Net_Profit']:,.2f} | {int(row['Total_Orders'])} | "
                f"₹{row['Average_Order_Value']:,.2f} |\n"
            )

        report += """
---

## 5. Payment Channel Profitability
| Payment Method | Avg Net Profit / Order | Total Net Profit | Total Revenue | Order Count |
| :--- | :--- | :--- | :--- | :--- |
"""
        for _, row in pay_summary.iterrows():
            report += (
                f"| {row['Payment_Method']} | ₹{row['Average_Net_Profit']:,.2f} | "
                f"₹{row['Total_Net_Profit']:,.2f} | ₹{row['Total_Revenue']:,.2f} | "
                f"{int(row['Transaction_Count'])} |\n"
            )

        report += f"""
---

## 6. Extreme Outliers & Records
- **Top Revenue Transaction**:
  - ID: `{highest['transaction_id']}` | Product: **{highest['product_name']}** ({highest['category']})
  - Location: **{highest['store_city']}** | Revenue: **₹{highest['revenue']:,.2f}** | Profit: **₹{highest['net_profit']:,.2f}**
- **Lowest Revenue Transaction**:
  - ID: `{lowest['transaction_id']}` | Product: **{lowest['product_name']}** ({lowest['category']})
  - Location: **{lowest['store_city']}** | Revenue: **₹{lowest['revenue']:,.2f}** | Profit: **₹{lowest['net_profit']:,.2f}**

---

## 7. Generated Visualizations
The following high-resolution charts are saved in `reports/figures/`:
1. `01_daily_revenue_trend.png` - Daily sales timeline with 7-day moving average.
2. `02_city_revenue_comparison.png` - Regional sales performance comparison.
3. `03_category_revenue_pie.png` - Revenue contribution by product category.
4. `04_unit_price_vs_quantity_scatter.png` - Basket analysis: Unit Price vs Quantity purchased.
5. `05_payment_profitability.png` - Mean net profit across payment gateways.
"""
        return report

    def build_html_dashboard(self) -> str:
        kpis = self.analytics.get_kpi_summary()
        cat_summary = self.analytics.get_category_summary()
        city_summary = self.analytics.get_city_summary()
        pay_summary = self.analytics.get_payment_method_summary()
        extremes = self.analytics.get_extreme_transactions()
        highest = extremes["highest_revenue_order"]
        lowest = extremes["lowest_revenue_order"]

        cat_rows = "".join(
            f"<tr><td><strong>{row['Category']}</strong></td>"
            f"<td>₹{row['Total_Revenue']:,.2f}</td>"
            f"<td>₹{row['Average_Revenue']:,.2f}</td>"
            f"<td>{int(row['Number_of_Sales'])}</td>"
            f"<td>₹{row['Total_Net_Profit']:,.2f}</td>"
            f"<td><span class='badge'>{row['Avg_Profit_Margin_Pct']}%</span></td></tr>"
            for _, row in cat_summary.iterrows()
        )

        city_rows = "".join(
            f"<tr><td><strong>{row['Store_City']}</strong></td>"
            f"<td>₹{row['Total_Revenue']:,.2f}</td>"
            f"<td>₹{row['Total_Net_Profit']:,.2f}</td>"
            f"<td>{int(row['Total_Orders'])}</td>"
            f"<td>₹{row['Average_Order_Value']:,.2f}</td></tr>"
            for _, row in city_summary.iterrows()
        )

        pay_rows = "".join(
            f"<tr><td><strong>{row['Payment_Method']}</strong></td>"
            f"<td>₹{row['Average_Net_Profit']:,.2f}</td>"
            f"<td>₹{row['Total_Net_Profit']:,.2f}</td>"
            f"<td>₹{row['Total_Revenue']:,.2f}</td>"
            f"<td>{int(row['Transaction_Count'])}</td></tr>"
            for _, row in pay_summary.iterrows()
        )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Sales Intelligence Dashboard</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --accent: #2563eb;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            padding: 30px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        h1 {{ font-size: 26px; font-weight: 700; color: #0f172a; }}
        .subtitle {{ font-size: 14px; color: var(--text-muted); margin-top: 4px; }}
        .badge-live {{
            background: #dcfce7;
            color: #15803d;
            font-size: 12px;
            font-weight: 600;
            padding: 5px 12px;
            border-radius: 20px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .kpi-title {{ font-size: 13px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-value {{ font-size: 26px; font-weight: 700; margin-top: 8px; color: #0f172a; }}
        .kpi-subtitle {{ font-size: 12px; color: var(--text-muted); margin-top: 5px; }}
        .card {{
            background: var(--bg-card);
            padding: 24px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 25px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .card-title {{ font-size: 18px; font-weight: 700; margin-bottom: 18px; color: #0f172a; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th {{
            text-align: left;
            padding: 12px 14px;
            background: #f1f5f9;
            color: #475569;
            font-weight: 600;
            border-bottom: 1px solid var(--border);
        }}
        td {{
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
        }}
        tr:hover td {{ background: #f8fafc; }}
        .badge {{
            background: #e0f2fe;
            color: #0369a1;
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 12px;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }}
        .chart-box {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }}
        .chart-box img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
        }}
        .extremes-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        .extreme-card {{
            background: #f8fafc;
            border-left: 4px solid var(--accent);
            padding: 15px;
            border-radius: 6px;
        }}
        .extreme-card.low {{ border-left-color: #ef4444; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>Retail Sales Analytics & Intelligence Dashboard</h1>
                <div class="subtitle">Comprehensive Analysis across Products, Geographies, and Channels</div>
            </div>
            <div class="badge-live">Automated Report Ready</div>
        </header>

        <section class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Total Gross Revenue</div>
                <div class="kpi-value">₹{kpis['total_revenue']:,.0f}</div>
                <div class="kpi-subtitle">Across {kpis['total_transactions']:,} transactions</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total Net Profit</div>
                <div class="kpi-value" style="color: #10b981;">₹{kpis['total_net_profit']:,.0f}</div>
                <div class="kpi-subtitle">{kpis['overall_profit_margin_pct']}% Overall Margin</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Average Order Value</div>
                <div class="kpi-value">₹{kpis['average_order_value']:,.0f}</div>
                <div class="kpi-subtitle">₹{kpis['total_revenue']/kpis['unique_products']:,.0f} avg per product</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">High-Value Orders</div>
                <div class="kpi-value">{kpis['high_value_orders_count']}</div>
                <div class="kpi-subtitle">{kpis['high_value_orders_pct']}% of orders > ₹5,000</div>
            </div>
        </section>

        <section class="card">
            <div class="card-title">Performance by Product Category</div>
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Total Revenue</th>
                        <th>Average Revenue</th>
                        <th>Orders</th>
                        <th>Net Profit</th>
                        <th>Avg Margin</th>
                    </tr>
                </thead>
                <tbody>
                    {cat_rows}
                </tbody>
            </table>
        </section>

        <section class="card">
            <div class="card-title">Geographic Performance by Store City</div>
            <table>
                <thead>
                    <tr>
                        <th>City</th>
                        <th>Total Revenue</th>
                        <th>Net Profit</th>
                        <th>Total Orders</th>
                        <th>Avg Order Value</th>
                    </tr>
                </thead>
                <tbody>
                    {city_rows}
                </tbody>
            </table>
        </section>

        <section class="card">
            <div class="card-title">Payment Method Profitability</div>
            <table>
                <thead>
                    <tr>
                        <th>Payment Method</th>
                        <th>Avg Net Profit / Order</th>
                        <th>Total Net Profit</th>
                        <th>Total Revenue</th>
                        <th>Order Count</th>
                    </tr>
                </thead>
                <tbody>
                    {pay_rows}
                </tbody>
            </table>
        </section>

        <section class="card">
            <div class="card-title">Transaction Records & Outliers</div>
            <div class="extremes-grid">
                <div class="extreme-card">
                    <h3 style="font-size: 15px; color: #2563eb; margin-bottom: 6px;">Highest Revenue Order</h3>
                    <p><strong>Order ID:</strong> {highest['transaction_id']}</p>
                    <p><strong>Product:</strong> {highest['product_name']} ({highest['category']})</p>
                    <p><strong>Location:</strong> {highest['store_city']}</p>
                    <p><strong>Revenue:</strong> ₹{highest['revenue']:,.2f} | <strong>Profit:</strong> ₹{highest['net_profit']:,.2f}</p>
                </div>
                <div class="extreme-card low">
                    <h3 style="font-size: 15px; color: #ef4444; margin-bottom: 6px;">Lowest Revenue Order</h3>
                    <p><strong>Order ID:</strong> {lowest['transaction_id']}</p>
                    <p><strong>Product:</strong> {lowest['product_name']} ({lowest['category']})</p>
                    <p><strong>Location:</strong> {lowest['store_city']}</p>
                    <p><strong>Revenue:</strong> ₹{lowest['revenue']:,.2f} | <strong>Profit:</strong> ₹{lowest['net_profit']:,.2f}</p>
                </div>
            </div>
        </section>

        <section class="card">
            <div class="card-title">Analytical Visualizations</div>
            <div class="charts-grid">
                <div class="chart-box">
                    <h4 style="margin-bottom: 10px;">Daily Sales Revenue Trend</h4>
                    <img src="figures/01_daily_revenue_trend.png" alt="Daily Sales Trend">
                </div>
                <div class="chart-box">
                    <h4 style="margin-bottom: 10px;">City Revenue Comparison</h4>
                    <img src="figures/02_city_revenue_comparison.png" alt="City Revenue Comparison">
                </div>
                <div class="chart-box">
                    <h4 style="margin-bottom: 10px;">Category Revenue Contribution</h4>
                    <img src="figures/03_category_revenue_pie.png" alt="Category Revenue Share">
                </div>
                <div class="chart-box">
                    <h4 style="margin-bottom: 10px;">Unit Price vs Quantity Purchased</h4>
                    <img src="figures/04_unit_price_vs_quantity_scatter.png" alt="Price vs Quantity">
                </div>
                <div class="chart-box" style="grid-column: 1 / -1;">
                    <h4 style="margin-bottom: 10px;">Average Net Profit by Payment Method</h4>
                    <img src="figures/05_payment_profitability.png" alt="Payment Profitability">
                </div>
            </div>
        </section>
    </div>
</body>
</html>
"""
        return html

    def save_report(self) -> Path:
        content = self.build_markdown_report()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Executive report saved to: {self.output_path}")

        # Also save HTML dashboard
        html_content = self.build_html_dashboard()
        html_path = self.output_path.parent / "dashboard.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"Interactive HTML dashboard saved to: {html_path}")

        return self.output_path
