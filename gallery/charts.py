"""Six chart recipes. Each draws on an existing Matplotlib Axes."""

import matplotlib.dates as mdates
import numpy as np
import pandas as pd

from .style import NAVY, TEAL, OCHRE, MUTED, PALETTE


def daily_trend(ax, data):
    frame = data["daily_trips"]
    dates = pd.to_datetime(frame["date"])
    ax.plot(dates, frame["trips"], color="#AABEC8", linewidth=1, label="Daily count")
    ax.plot(dates, frame["trips"].rolling(7, min_periods=7).mean(), color=TEAL, linewidth=2.4, label="Trailing 7-day mean")
    ax.set(xlabel="Date · 2026", ylabel="Trips / day", ylim=(0, None))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.grid(axis="y")
    ax.legend(frameon=False, fontsize=8, loc="lower left")


def spending_bars(ax, data):
    values = data["spending"].groupby("category")["amount_cu"].mean().sort_values()
    bars = ax.barh(values.index, values.values, color=[TEAL] * (len(values) - 1) + [NAVY], height=.56)
    for bar, value in zip(bars, values):
        ax.text(value + 6, bar.get_y() + bar.get_height() / 2, f"{value:.0f}", va="center", fontsize=10, color=NAVY)
    ax.set(xlabel="Mean monthly spending (currency units)", xlim=(0, values.max() * 1.22))
    ax.grid(axis="x")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)


def duration_histogram(ax, data):
    values = data["commutes"]["duration_min"]
    edges = np.arange(0, np.ceil(values.max() / 5) * 5 + 5, 5)
    ax.hist(values, bins=edges, color=TEAL, edgecolor="white", linewidth=1)
    median = values.median()
    ax.axvline(median, color=NAVY, linestyle="--", linewidth=1.6, label=f"Median: {median:.1f} min")
    ax.set(xlabel="Commute duration (minutes)", ylabel="Observations", xlim=(0, edges[-1]))
    ax.legend(frameon=False, fontsize=8)
    ax.grid(axis="y")


def activity_heatmap(ax, data):
    order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    matrix = data["activity"].pivot(index="weekday", columns="hour", values="events").loc[order]
    im = ax.imshow(matrix, aspect="auto", cmap="viridis", vmin=0, vmax=int(matrix.to_numpy().max()), interpolation="nearest")
    ax.set(yticks=np.arange(7), yticklabels=order, xticks=np.arange(0, 24, 4), xticklabels=["00", "04", "08", "12", "16", "20"], xlabel="Hour of day")
    ax.tick_params(length=0)
    ax.figure.colorbar(im, ax=ax, fraction=.035, pad=.03, label="Events")
    for spine in ax.spines.values():
        spine.set_visible(False)


def distance_scatter(ax, data):
    markers = {"Walk": "o", "Cycle": "s", "Transit": "^"}
    for mode, color in PALETTE.items():
        frame = data["commutes"].query("mode == @mode")
        ax.scatter(frame["distance_km"], frame["duration_min"], c=color, marker=markers[mode], label=mode, s=22, alpha=.65, linewidths=0)
    ax.set(xlabel="Distance (km)", ylabel="Duration (minutes)", xlim=(0, None), ylim=(0, None))
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.grid(alpha=.7)


def mode_boxplot(ax, data):
    modes = list(PALETTE)
    values = [data["commutes"].query("mode == @mode")["duration_min"] for mode in modes]
    boxes = ax.boxplot(
        values, tick_labels=modes, widths=.48, patch_artist=True, whis=1.5,
        medianprops={"color": "white", "linewidth": 2},
        flierprops={"marker": ".", "markersize": 4, "markeredgecolor": MUTED},
        whiskerprops={"color": MUTED}, capprops={"color": MUTED},
    )
    for patch, color in zip(boxes["boxes"], PALETTE.values()):
        patch.set_facecolor(color)
        patch.set_edgecolor(color)
    ax.set(ylabel="Commute duration (minutes)", ylim=(0, None))
    ax.grid(axis="y")


RECIPES = [
    ("01-daily-trend", "A daily rhythm", "90 days · trailing 7-day average", daily_trend),
    ("02-spending-bars", "Where the budget goes", "12 months · category means", spending_bars),
    ("03-duration-histogram", "How long is a commute?", "360 trips · 5-minute bins", duration_histogram),
    ("04-activity-heatmap", "Patterns across the week", "168 weekday-hour cells · simulated event counts", activity_heatmap),
    ("05-distance-scatter", "Distance meets duration", "360 trips · color and shape encode mode", distance_scatter),
    ("06-mode-boxplot", "Three ways to get there", "120 trips per mode · whiskers at 1.5 × IQR", mode_boxplot),
]
