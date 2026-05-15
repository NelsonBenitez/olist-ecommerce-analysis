# %% [markdown]
# # Notebook 5 — Summary & Business Recommendations
#
# **Project:** Olist E-Commerce — Sales Funnel & RFM Analysis
# **Author:** Your Name
# **Date:** 2024

# %% [markdown]
# ## Key Findings
#
# *(Fill in after running notebooks 01–04)*
#
# | # | Finding | Impact |
# |---|---------|--------|
# | 1 | Funnel drop-off: X% of orders never get reviewed | Lost feedback loop |
# | 2 | Champions segment = X% of customers, Y% of revenue | High concentration risk |
# | 3 | Late deliveries (>3 days) → avg review score drops from X to Y | Churn driver |
# | 4 | At Risk segment: X customers, R$ Y in at-risk revenue | Retention opportunity |

# %% [markdown]
# ## Recommendations
#
# 1. **Retention campaign for At Risk segment** — offer a 10% discount voucher to customers
#    with R≤2, F≥3. Estimated revenue at risk: R$ [X].
#
# 2. **Delivery SLA improvement** — the data shows review scores drop sharply beyond 3 days late.
#    Prioritise logistics partnerships in states with highest delay rates.
#
# 3. **Champions loyalty programme** — Champions generate disproportionate revenue.
#    A VIP tier (free shipping, early access) can lock in this segment.
#
# 4. **New Customer nurture** — high recency, low frequency. A second-purchase incentive
#    within 30 days of first order can move them to Potential Loyalist.

# %%
import pandas as pd

# Load processed outputs
rfm = pd.read_csv("../data/processed/rfm_segmented.csv")
seg = pd.read_csv("../data/processed/segment_summary.csv")

print("=== SEGMENT SUMMARY ===")
print(seg.sort_values("total_revenue", ascending=False).to_string(index=False))

print("\n=== TOP HYPOTHESIS RESULT ===")
top_pct    = seg.nlargest(1, "revenue_share_pct")["revenue_share_pct"].values[0]
top_seg    = seg.nlargest(1, "revenue_share_pct")["segment"].values[0]
top_cust   = seg.nlargest(1, "revenue_share_pct")["customer_count"].values[0]
total_cust = seg["customer_count"].sum()
print(f"'{top_seg}' = {top_cust/total_cust*100:.1f}% of customers, {top_pct:.1f}% of revenue")
print(f"Hypothesis {'CONFIRMED' if top_pct > 40 else 'PARTIALLY CONFIRMED'}: top segment drives {top_pct:.0f}% of revenue")
