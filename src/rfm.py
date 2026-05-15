"""
rfm.py
RFM (Recency, Frequency, Monetary) scoring and segmentation.
"""
import pandas as pd
import numpy as np


def compute_rfm(orders_df, payments_df, snapshot_date=None):
    """
    Compute RFM values per customer.

    Parameters
    ----------
    orders_df   : orders table (must include order_purchase_timestamp, customer_id)
    payments_df : payments table (must include order_id, payment_value)
    snapshot_date : reference date for recency. Defaults to max order date + 1 day.

    Returns
    -------
    DataFrame with columns: customer_id, recency, frequency, monetary
    """
    # Only use delivered orders
    delivered = orders_df[orders_df["order_status"] == "delivered"].copy()

    # Join payments to get revenue per order
    order_revenue = (
        payments_df.groupby("order_id")["payment_value"]
        .sum()
        .reset_index()
        .rename(columns={"payment_value": "revenue"})
    )
    delivered = delivered.merge(order_revenue, on="order_id", how="left")

    if snapshot_date is None:
        snapshot_date = delivered["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm = (
        delivered.groupby("customer_id")
        .agg(
            recency=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
            frequency=("order_id", "count"),
            monetary=("revenue", "sum"),
        )
        .reset_index()
    )
    return rfm


def score_rfm(rfm_df, n_quantiles=5):
    """
    Add R, F, M scores (1–5) and a combined RFM score.
    Higher = better for all three dimensions.
    """
    df = rfm_df.copy()

    # Recency: lower days = better = higher score
    df["r_score"] = pd.qcut(df["recency"], n_quantiles, labels=range(n_quantiles, 0, -1), duplicates="drop")
    df["f_score"] = pd.qcut(df["frequency"].rank(method="first"), n_quantiles, labels=range(1, n_quantiles + 1), duplicates="drop")
    df["m_score"] = pd.qcut(df["monetary"].rank(method="first"), n_quantiles, labels=range(1, n_quantiles + 1), duplicates="drop")

    for col in ["r_score", "f_score", "m_score"]:
        df[col] = df[col].astype(int)

    df["rfm_score"] = df["r_score"] * 100 + df["f_score"] * 10 + df["m_score"]
    return df


SEGMENT_MAP = {
    "Champions":         lambda r, f, m: (r >= 4) & (f >= 4) & (m >= 4),
    "Loyal":             lambda r, f, m: (f >= 4) & (m >= 3),
    "Potential Loyalist":lambda r, f, m: (r >= 3) & (f <= 3),
    "At Risk":           lambda r, f, m: (r <= 2) & (f >= 3),
    "Lost":              lambda r, f, m: (r == 1) & (f == 1),
    "New Customers":     lambda r, f, m: (r >= 4) & (f == 1),
}


def assign_segments(scored_df):
    """Assign a human-readable segment label to each customer."""
    df = scored_df.copy()
    df["segment"] = "Other"
    for label, condition in SEGMENT_MAP.items():
        mask = condition(df["r_score"], df["f_score"], df["m_score"])
        df.loc[mask, "segment"] = label
    return df
