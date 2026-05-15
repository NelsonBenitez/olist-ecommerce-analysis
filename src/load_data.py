"""
load_data.py
Helpers to load and validate all 9 Olist CSV files.
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

FILES = {
    "orders":       "olist_orders_dataset.csv",
    "order_items":  "olist_order_items_dataset.csv",
    "customers":    "olist_customers_dataset.csv",
    "products":     "olist_products_dataset.csv",
    "sellers":      "olist_sellers_dataset.csv",
    "payments":     "olist_order_payments_dataset.csv",
    "reviews":      "olist_order_reviews_dataset.csv",
    "category_t":   "product_category_name_translation.csv",
    "geolocation":  "olist_geolocation_dataset.csv",
}

DATE_COLS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def load_all(verbose=True):
    """Load all Olist tables. Returns a dict of DataFrames."""
    tables = {}
    for name, filename in FILES.items():
        path = DATA_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing: {path}\nDownload from Kaggle and place in data/raw/")
        tables[name] = pd.read_csv(path, low_memory=False)
        if verbose:
            print(f"  {name:15s} → {tables[name].shape[0]:>7,} rows")

    # Parse datetime columns in orders
    for col in DATE_COLS:
        if col in tables["orders"].columns:
            tables["orders"][col] = pd.to_datetime(tables["orders"][col])

    return tables


def load_table(name):
    """Load a single table by name."""
    if name not in FILES:
        raise ValueError(f"Unknown table '{name}'. Choose from: {list(FILES.keys())}")
    path = DATA_DIR / FILES[name]
    return pd.read_csv(path, low_memory=False)


def summarise(tables):
    """Print a quick data quality summary for all tables."""
    print(f"\n{'Table':<20} {'Rows':>8} {'Cols':>6} {'Nulls%':>8}")
    print("-" * 46)
    for name, df in tables.items():
        null_pct = (df.isnull().sum().sum() / df.size * 100)
        print(f"{name:<20} {df.shape[0]:>8,} {df.shape[1]:>6} {null_pct:>7.1f}%")
