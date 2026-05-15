"""
utils.py
Shared plotting and formatting utilities.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

PALETTE = {
    "blue":   "#378ADD",
    "teal":   "#1D9E75",
    "coral":  "#D85A30",
    "amber":  "#EF9F27",
    "purple": "#7F77DD",
    "gray":   "#888780",
}

sns.set_theme(style="whitegrid", palette=list(PALETTE.values()))


def fmt_brl(value, pos=None):
    """Format a number as Brazilian Real (R$)."""
    return f"R$ {value:,.0f}"


def plot_funnel(stages: dict, title="Purchase Funnel"):
    """
    Bar funnel chart.
    stages: dict of {stage_name: count}, ordered from broadest to narrowest.
    """
    labels = list(stages.keys())
    values = list(stages.values())
    colors = [PALETTE["blue"]] + [PALETTE["teal"]] * (len(labels) - 2) + [PALETTE["coral"]]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(labels[::-1], values[::-1], color=colors[::-1])

    for bar, val in zip(bars, values[::-1]):
        ax.text(val + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", fontsize=11)

    ax.set_xlabel("Orders")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    return fig


def plot_rfm_segments(segment_summary: pd.DataFrame):
    """
    Bar chart of customer count and revenue share by RFM segment.
    segment_summary must have columns: segment, customer_count, revenue_share_pct
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    seg = segment_summary.sort_values("customer_count", ascending=True)

    ax1.barh(seg["segment"], seg["customer_count"], color=PALETTE["blue"])
    ax1.set_title("Customers per segment", fontweight="bold")
    ax1.set_xlabel("Customers")

    ax2.barh(seg["segment"], seg["revenue_share_pct"], color=PALETTE["teal"])
    ax2.set_title("Revenue share (%)", fontweight="bold")
    ax2.set_xlabel("% of total revenue")

    for ax in [ax1, ax2]:
        sns.despine(ax=ax, left=True, bottom=True)

    plt.tight_layout()
    return fig
