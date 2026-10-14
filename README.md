# Retail Sales Analytics & Business Intelligence Engine

An enterprise-ready, modular Python data analytics framework transformed from exploratory scripts into a production-grade data pipeline. It performs automated ingestion, validation, vector mathematics, feature engineering, business intelligence aggregations, publication-quality visualizations, and executive reporting for retail transaction datasets.

---

## 📊 Executive Summary & Key Business Findings

Based on analysis of 800 transactions across Tamil Nadu retail hubs:

- **Gross Revenue**: **₹4,220,060.00** across 800 transactions (Average Order Value: **₹5,275.07**).
- **Net Profit**: **₹1,599,350.00** with an overall profit margin of **37.90%**.
- **High-Value Orders**: **326 orders (40.75%)** exceeded the **₹5,000** threshold.
- **Top Product Category**: **Electronics** generated the majority of revenue (**₹2,741,300**, 65.0% share), while **Stationery** delivered the highest margin efficiency (**49.75%**).
- **Top Geographic Hub**: **Tirunelveli** led in total revenue (**₹812,850**), while **Madurai** had the highest average order value (**₹6,213.97**).
- **Payment Method Profitability**: **Cash** and **Credit Card** yielded higher average net profits per transaction (**₹2,053.59** and **₹2,016.48**) compared to UPI (**₹1,942.28**).
- **Record Transaction**: Order `#TRX-2025-1152` (*Mechanical Keyboard*) generated the single highest transaction value of **₹19,200.00** (Net Profit: **₹6,400.00**).

---

## 🏗️ Project Architecture

```
retail_sales_analytics/
│
├── data/
│   ├── raw/                       # Original input data (Retail_Sales_Easy_Project.xlsx)
│   └── processed/                 # Cleaned & feature-engineered data (.csv and .xlsx)
│
├── src/
│   └── retail_sales_analytics/    # The importable Python module package
│       ├── __init__.py            # Clean top-level API exports
│       ├── __main__.py            # Direct execution entry point (python -m retail_sales_analytics)
│       ├── cli.py                 # CLI commands (retail-sales, retail-analytics)
│       ├── config.py              # Configurations, thresholds, and plot styling
│       ├── data_loader.py         # Ingestion with fallback resolution and schema validation
│       ├── data_processor.py      # Data cleaning, feature engineering, and segment extractors
│       ├── analytics.py           # Vector math (NumPy), aggregations, KPIs, and outlier detection
│       ├── visualizer.py          # Publication-quality charts (300 DPI) using Matplotlib & Seaborn
│       └── reporter.py            # Automated Executive Markdown & interactive HTML dashboard generator
│
├── reports/
│   ├── figures/                   # Exported high-res visualizations (PNG)
│   │   ├── 01_daily_revenue_trend.png
│   │   ├── 02_city_revenue_comparison.png
│   │   ├── 03_category_revenue_pie.png
│   │   ├── 04_unit_price_vs_quantity_scatter.png
│   │   └── 05_payment_profitability.png
│   ├── executive_summary.md       # Full executive markdown report
│   └── dashboard.html             # Standalone interactive HTML report with KPI tiles & charts
│
├── tests/
│   ├── __init__.py
│   ├── test_processor.py          # Unit tests for transformations, filters, and feature engineering
│   └── test_analytics.py          # Unit tests for NumPy statistics, aggregations, and KPIs
│
├── main.py                        # Convenience runner script
├── pyproject.toml                 # Standard PEP 518/621 packaging metadata & console entry points
├── setup.py                       # Setuptools configuration
├── requirements.txt               # Dependencies
├── README.md                      # Project documentation
└── .gitignore                     # Git ignore rules
```

---

## 📦 Python Module Installation & Usage

You can install this project as an editable Python package/module into your environment:

```bash
pip install -e .
```

Once installed, you can import and use it in **any** Python script, notebook, or application:

```python
import retail_sales_analytics as rsa

# 1. Ingest dataset with schema validation
df = rsa.load_data()

# 2. Execute cleaning & feature engineering (Net_Profit, Profit_Margin_Pct, Order_Label)
df_clean = rsa.process_pipeline(df)

# 3. Compute business KPIs and vector metrics
analytics = rsa.RetailAnalytics(df_clean)
kpis = analytics.get_kpi_summary()
print(f"Total Revenue: ₹{kpis['total_revenue']:,.2f}")
print(f"Profit Margin: {kpis['overall_profit_margin_pct']}%")

# 4. Filter targeted segments
electronics = rsa.get_category_subset(df_clean, "Electronics")
bulk_upi = rsa.get_bulk_orders_by_payment(df_clean, min_quantity=5, payment_method="UPI")

# 5. Generate high-res visual charts & executive reports
visualizer = rsa.RetailVisualizer(df_clean)
visualizer.generate_all_charts()

reporter = rsa.ReportGenerator(analytics)
reporter.save_report()
```

---

## 💻 CLI Usage

### Run via Module Execution
```bash
python -m retail_sales_analytics
```

### Run via Root Script
```bash
python main.py
```

### Run via Installed Console Command
```bash
retail-sales
# or
retail-analytics
```

### Custom Dataset File
Run the pipeline against another Excel or CSV file:
```bash
python main.py --file "path/to/custom_sales.xlsx"
```

### Display Plots Interactively
Pop up visualization windows during execution:
```bash
python main.py --show-plots
```

### Check Available Options
```bash
python main.py --help
```

---

## 🌐 Launch the Interactive Website

### Option A: Streamlit Data Science Web App
Run the interactive web app locally with dynamic filters, KPI tiles, custom dataset upload, and data explorer:
```bash
python -m streamlit run app.py
```
This will automatically launch the website in your browser at `http://localhost:8501`.

### Option B: Standalone Web Dashboard (GitHub Pages Ready)
Open `docs/index.html` directly in any web browser:
```powershell
Start-Process .\docs\index.html
```
Or serve it locally:
```bash
python -m http.server 8000 --directory docs
```

#### 🚀 Publish to GitHub Pages (Live on the Internet)
Your repository is pre-configured to host this website for free on GitHub Pages:
1. Open your repository settings: [github.com/ramanan67/retail-sales-analyst/settings/pages](https://github.com/ramanan67/retail-sales-analyst/settings/pages)
2. Under **Build and deployment > Branch**, select **`main`** branch and the **`/docs`** folder.
3. Click **Save**.
4. In ~60 seconds, your site will be live at:
   👉 `https://ramanan67.github.io/retail-sales-analyst/`

---

## 🧪 Running Unit Tests

Run the test suite with `pytest`:
```bash
python -m pytest tests/ -v
```

All 8 test suites verify:
- Data type conversions and whitespace cleaning
- Net profit, profit margin %, and order value segmentation logic
- Specialized filters (Electronics, UPI bulk orders, Target cities)
- NumPy 1D and 2D vector computations and cumulative sums
- Business KPIs and extreme transaction detection

---

## 📈 Generated Visualizations

All charts are saved in `reports/figures/` at 300 DPI:

1. **`01_daily_revenue_trend.png`**: Daily revenue progression across the 6-month period with a 7-day moving trend line.
2. **`02_city_revenue_comparison.png`**: Total revenue generated by store location with value annotations.
3. **`03_category_revenue_pie.png`**: Revenue share breakdown among Electronics, Accessories, and Stationery.
4. **`04_unit_price_vs_quantity_scatter.png`**: Transaction cluster distribution showing purchasing patterns.
5. **`05_payment_profitability.png`**: Comparison of average net profit generated across Cash, Credit Card, Debit Card, and UPI.

---

## 📄 Automated Reports

- **Executive Markdown Report**: `reports/executive_summary.md`
- **Interactive HTML Dashboard**: `reports/dashboard.html` (Open directly in any modern browser for a clean UI overview).
