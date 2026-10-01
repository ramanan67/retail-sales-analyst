from pathlib import Path

# Base project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Ensure directories exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Dataset file locations
DEFAULT_DATA_FILENAME = "Retail_Sales_Easy_Project.xlsx"
LOCAL_DATASET_PATH = RAW_DATA_DIR / DEFAULT_DATA_FILENAME
EXTERNAL_DATASET_PATH = Path(r"C:\Users\raman\Documents\py lib\Retail_Sales_Easy_Project.xlsx")

# Output files
PROCESSED_DATASET_CSV = PROCESSED_DATA_DIR / "retail_sales_processed.csv"
PROCESSED_DATASET_EXCEL = PROCESSED_DATA_DIR / "retail_sales_processed.xlsx"
EXECUTIVE_SUMMARY_REPORT = REPORTS_DIR / "executive_summary.md"

# Business logic thresholds & segments
HIGH_VALUE_THRESHOLD = 5000.0
CORE_TARGET_CITIES = ["Chennai", "Coimbatore", "Madurai"]

# Visualization aesthetics
PLOT_STYLE = "seaborn-v0_8-whitegrid"
DEFAULT_DPI = 300
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
COLOR_PALETTE = "viridis"
