# Executive Retail Sales Performance Report

## 1. Key Performance Indicators (KPIs)
| Metric | Value |
| :--- | :--- |
| **Total Transactions Analyzed** | 800 |
| **Total Gross Revenue** | ₹4,220,060.00 |
| **Total Net Profit** | ₹1,599,350.00 |
| **Overall Profit Margin** | 37.9% |
| **Average Order Value (AOV)** | ₹5,275.07 |
| **High-Value Orders (> ₹5,000)** | 320 (40.0%) |
| **Unique Product Lines** | 12 |
| **Store Locations (Cities)** | 6 |

---

## 2. Statistical Distribution (Revenue Vector Analysis)
- **Vector Sum**: ₹4,220,060.00
- **Mean Revenue**: ₹5,275.07
- **Median Revenue**: ₹3,600.00
- **Standard Deviation**: ₹4,488.20
- **Variance**: 20,143,982.49
- **Min / Max Revenue**: ₹250.00 / ₹19,200.00

---

## 3. Product Category Breakdown
| Category | Total Revenue | Avg Revenue | Orders | Net Profit | Avg Margin % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Electronics | ₹2,741,300.00 | ₹7,011.00 | 391 | ₹971,450.00 | 35.68% |
| Accessories | ₹1,009,050.00 | ₹6,864.29 | 147 | ₹396,700.00 | 39.4% |
| Stationery | ₹469,710.00 | ₹1,792.79 | 262 | ₹231,200.00 | 49.75% |

---

## 4. Geographic Performance by City
| City | Total Revenue | Net Profit | Total Orders | Average Order Value |
| :--- | :--- | :--- | :--- | :--- |
| Tirunelveli | ₹812,850.00 | ₹308,480.00 | 151 | ₹5,383.11 |
| Madurai | ₹751,890.00 | ₹277,640.00 | 121 | ₹6,213.97 |
| Chennai | ₹700,980.00 | ₹264,860.00 | 121 | ₹5,793.22 |
| Salem | ₹661,160.00 | ₹251,870.00 | 135 | ₹4,897.48 |
| Trichy | ₹650,810.00 | ₹250,050.00 | 138 | ₹4,716.01 |
| Coimbatore | ₹642,370.00 | ₹246,450.00 | 134 | ₹4,793.81 |

---

## 5. Payment Channel Profitability
| Payment Method | Avg Net Profit / Order | Total Net Profit | Total Revenue | Order Count |
| :--- | :--- | :--- | :--- | :--- |
| Cash | ₹2,053.59 | ₹423,040.00 | ₹1,119,490.00 | 206 |
| Credit Card | ₹2,016.48 | ₹429,510.00 | ₹1,128,380.00 | 213 |
| Debit Card | ₹1,978.40 | ₹371,940.00 | ₹988,250.00 | 188 |
| UPI | ₹1,942.28 | ₹374,860.00 | ₹983,940.00 | 193 |

---

## 6. Extreme Outliers & Records
- **Top Revenue Transaction**:
  - ID: `TRX-2025-1152` | Product: **Mechanical Keyboard** (Electronics)
  - Location: **Tirunelveli** | Revenue: **₹19,200.00** | Profit: **₹6,400.00**
- **Lowest Revenue Transaction**:
  - ID: `TRX-2025-1003` | Product: **Gel Pen Pack (Pack of 10)** (Stationery)
  - Location: **Chennai** | Revenue: **₹250.00** | Profit: **₹130.00**

---

## 7. Generated Visualizations
The following high-resolution charts are saved in `reports/figures/`:
1. `01_daily_revenue_trend.png` - Daily sales timeline with 7-day moving average.
2. `02_city_revenue_comparison.png` - Regional sales performance comparison.
3. `03_category_revenue_pie.png` - Revenue contribution by product category.
4. `04_unit_price_vs_quantity_scatter.png` - Basket analysis: Unit Price vs Quantity purchased.
5. `05_payment_profitability.png` - Mean net profit across payment gateways.
