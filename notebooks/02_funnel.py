# %% [markdown]
# # Notebook 2 — Sales Funnel Analysis
# **Hypothesis:** Where do customers drop off between placing an order and leaving a review?

# %%
import sys
sys.path.append("../src")

import pandas as pd
import matplotlib.pyplot as plt
from load_data import load_all
from utils import plot_funnel

tables  = load_all(verbose=False)
orders  = tables["orders"]
reviews = tables["reviews"]

# %% [markdown]
# ## 1. Build the funnel stages

# %%
funnel = {
    "1. Order placed":    len(orders),
    "2. Order approved":  orders["order_approved_at"].notna().sum(),
    "3. Shipped":         orders["order_delivered_carrier_date"].notna().sum(),
    "4. Delivered":       (orders["order_status"] == "delivered").sum(),
    "5. Review left":     reviews["review_score"].notna().sum(),
}

for stage, count in funnel.items():
    print(f"  {stage}: {count:,}")

# %% [markdown]
# ## 2. Conversion rates between stages

# %%
stages = list(funnel.values())
labels = list(funnel.keys())

for i in range(1, len(stages)):
    conv = stages[i] / stages[i - 1] * 100
    print(f"  {labels[i-1]} → {labels[i]}: {conv:.1f}%")

# %% [markdown]
# ## 3. Funnel chart

# %%
fig = plot_funnel(funnel, title="Olist Purchase Funnel")
plt.savefig("../reports/02_funnel.png", dpi=150)
plt.show()

# %% [markdown]
# ## 4. Revenue by order status (what's stuck?)

# %%
payments = tables["payments"]
status_revenue = (
    orders.merge(payments.groupby("order_id")["payment_value"].sum().reset_index(), on="order_id")
    .groupby("order_status")["payment_value"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "revenue", "count": "orders"})
    .sort_values("revenue", ascending=False)
)
print(status_revenue.round(2))

# %% [markdown]
# ## Next step → Notebook 03: RFM Segmentation
