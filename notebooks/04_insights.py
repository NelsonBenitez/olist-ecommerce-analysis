# %% [markdown]
# # Notebook 4 — Insights: Delivery Delay & Review Scores
# **Question:** Does late delivery kill customer satisfaction? Quantify the relationship.

# %%
import sys
sys.path.append("../src")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from load_data import load_all

tables   = load_all(verbose=False)
orders   = tables["orders"]
reviews  = tables["reviews"]
payments = tables["payments"]

# %% [markdown]
# ## 1. Merge orders with reviews and compute delay

# %%
df = orders.merge(reviews[["order_id", "review_score"]], on="order_id", how="inner")
df = df[df["order_status"] == "delivered"].copy()

df["delivery_delay_days"] = (
    df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
).dt.days

df = df.dropna(subset=["delivery_delay_days", "review_score"])
print(f"Analysing {len(df):,} delivered + reviewed orders")

# %% [markdown]
# ## 2. Correlation test

# %%
corr, p_value = stats.pearsonr(df["delivery_delay_days"], df["review_score"])
print(f"\nPearson correlation: {corr:.3f}")
print(f"P-value: {p_value:.2e}")
print(f"Interpretation: {'Significant' if p_value < 0.05 else 'Not significant'} negative correlation")

# %% [markdown]
# ## 3. Average review score by delay bucket

# %%
df["delay_bucket"] = pd.cut(
    df["delivery_delay_days"],
    bins=[-999, -7, -3, 0, 3, 7, 999],
    labels=["Early 7d+", "Early 3-7d", "On time", "Late 1-3d", "Late 4-7d", "Late 7d+"]
)

delay_review = df.groupby("delay_bucket", observed=True).agg(
    orders=("order_id", "count"),
    avg_score=("review_score", "mean"),
).reset_index()

print(delay_review.round(2))

fig, ax = plt.subplots(figsize=(9, 4))
colors = ["#1D9E75", "#1D9E75", "#378ADD", "#EF9F27", "#D85A30", "#993C1D"]
ax.bar(delay_review["delay_bucket"].astype(str), delay_review["avg_score"], color=colors)
ax.axhline(df["review_score"].mean(), color="gray", linestyle="--", label=f"Overall avg: {df['review_score'].mean():.2f}")
ax.set_ylim(1, 5.5)
ax.set_title("Avg review score by delivery timing", fontsize=13, fontweight="bold")
ax.set_xlabel("Delivery vs. estimated date")
ax.set_ylabel("Review score (1–5)")
ax.legend()
plt.tight_layout()
plt.savefig("../reports/04_delay_vs_review.png", dpi=150)
plt.show()

# %% [markdown]
# ## Next step → Notebook 05: Summary & Recommendations
