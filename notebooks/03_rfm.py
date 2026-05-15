# %% [markdown]
# # Notebook 3 — RFM Segmentation
# **Goal:** Score every customer on Recency, Frequency, Monetary value and assign segments.

# %%
import sys
sys.path.append("../src")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from load_data import load_all
from rfm import compute_rfm, score_rfm, assign_segments
from utils import plot_rfm_segments

tables   = load_all(verbose=False)
orders   = tables["orders"]
payments = tables["payments"]

# %% [markdown]
# ## 1. Compute RFM values

# %%
rfm = compute_rfm(orders, payments)
print(rfm.describe().round(2))

# %% [markdown]
# ## 2. Score and segment

# %%
rfm_scored    = score_rfm(rfm)
rfm_segmented = assign_segments(rfm_scored)

print("\nSegment distribution:")
print(rfm_segmented["segment"].value_counts())

# %% [markdown]
# ## 3. Revenue and LTV by segment

# %%
segment_summary = (
    rfm_segmented.groupby("segment")
    .agg(
        customer_count=("customer_id", "count"),
        avg_monetary=("monetary", "mean"),
        total_revenue=("monetary", "sum"),
        avg_frequency=("frequency", "mean"),
        avg_recency=("recency", "mean"),
    )
    .reset_index()
)
segment_summary["revenue_share_pct"] = (
    segment_summary["total_revenue"] / segment_summary["total_revenue"].sum() * 100
).round(1)

print(segment_summary.sort_values("total_revenue", ascending=False).round(2).to_string())

# %% [markdown]
# ## 4. Visualise segments

# %%
fig = plot_rfm_segments(segment_summary)
plt.savefig("../reports/03_rfm_segments.png", dpi=150)
plt.show()

# %% [markdown]
# ## 5. Save segmented data for dashboard

# %%
rfm_segmented.to_csv("../data/processed/rfm_segmented.csv", index=False)
segment_summary.to_csv("../data/processed/segment_summary.csv", index=False)
print("Saved to data/processed/")

# %% [markdown]
# ## Next step → Notebook 04: Insights & Delivery Analysis
