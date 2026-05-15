# %% [markdown]
# # Notebook 1 — Data Loading & Exploration
# **Goal:** Load all 9 Olist tables, validate data quality, and understand the schema.

# %%
import sys
sys.path.append("../src")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from load_data import load_all, summarise

# %% [markdown]
# ## 1. Load all tables

# %%
print("Loading Olist tables...\n")
tables = load_all(verbose=True)

orders      = tables["orders"]
order_items = tables["order_items"]
customers   = tables["customers"]
products    = tables["products"]
sellers     = tables["sellers"]
payments    = tables["payments"]
reviews     = tables["reviews"]
category_t  = tables["category_t"]

# %% [markdown]
# ## 2. Data quality summary

# %%
summarise(tables)

# %% [markdown]
# ## 3. Orders deep-dive

# %%
# Date range
print("Date range:")
print("  From:", orders["order_purchase_timestamp"].min())
print("  To:  ", orders["order_purchase_timestamp"].max())

# Status distribution
print("\nOrder status breakdown:")
print(orders["order_status"].value_counts())

# %% [markdown]
# ## 4. Orders over time

# %%
orders["month"] = orders["order_purchase_timestamp"].dt.to_period("M")
monthly = orders.groupby("month").size().reset_index(name="orders")

fig, ax = plt.subplots(figsize=(12, 4))
ax.bar(monthly["month"].astype(str), monthly["orders"], color="#378ADD")
ax.set_title("Orders per month", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Orders")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../reports/01_orders_over_time.png", dpi=150)
plt.show()

# %% [markdown]
# ## 5. Schema relationship check

# %%
print("Key relationship check:")
print(f"  Orders in order_items not in orders: {order_items[~order_items['order_id'].isin(orders['order_id'])].shape[0]}")
print(f"  Orders in payments not in orders:    {payments[~payments['order_id'].isin(orders['order_id'])].shape[0]}")
print(f"  Orders in reviews not in orders:     {reviews[~reviews['order_id'].isin(orders['order_id'])].shape[0]}")

# %% [markdown]
# ## Next step → Notebook 02: Sales Funnel Analysis
