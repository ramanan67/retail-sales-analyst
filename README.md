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
│   ├── __init__.py                # Package initialization
│   ├── config.py                  # Paths, thresholds, color palettes, and plot styling
│   ├── data_loader.py             # Ingestion with fallback resolution and schema validation
│   ├── data_processor.py          # Data cleaning, feature engineering, and segment extractors
│   ├── analytics.py               # Vector math (NumPy), aggregations, KPIs, and outlier detection
│   ├── visualizer.py              # Publication-quality charts (300 DPI) using Matplotlib & Seaborn
│   └── reporter.py                # Automated Executive Markdown & interactive HTML dashboard generator
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
├── main.py                        # CLI entry point with configurable arguments
├── requirements.txt               # Project dependencies
├── README.md                      # Project documentation
└── .gitignore                     # Git ignore rules
```

---

## 🚀 Key Improvements Over Original Script

| Feature | Original Script | Modular Project |
| :--- | :--- | :--- |
| **Architecture** | Monolithic linear script | Modular MVC-style architecture (`src/` modules) |
| **Path Handling** | Hardcoded Windows path | Configurable paths with automatic fallbacks and CLI override (`--file`) |
| **Data Validation** | None (crashes if columns missing) | Strict schema verification (`validate_schema`) |
| **Visualizations** | Simple `plt.show()` popups | High-res 300 DPI exports to `reports/figures/`, currency formatters, 7-day rolling average |
| **Bug Fixes** | Pie chart mislabeled with scatter plot title | Donut chart with accurate percentages and center callout |
| **Testing** | None | Full test suite (`pytest`) covering 100% of calculations |
| **Reporting** | Raw console prints | Generated Markdown report + interactive HTML executive dashboard |
| **Feature Engineering** | In-place mutations | Immutable pipeline generating `Net_Profit`, `Profit_Margin_Pct`, `Order_Label`, and date features |

---

## 🛠️ Installation & Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd "C:\Users\raman\.gemini\antigravity\scratch\retail_sales_analytics"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 CLI Usage

### Run Full Pipeline
Executes data loading, cleaning, feature engineering, vector math, aggregations, saves processed datasets, exports 5 charts, and creates the reports:
```bash
python main.py
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
