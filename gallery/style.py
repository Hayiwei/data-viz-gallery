"""A restrained palette and reusable figure typography."""

import matplotlib as mpl

NAVY = "#19334A"
TEAL = "#117C83"
OCHRE = "#B97932"
MUTED = "#596E7C"
PALETTE = {"Walk": TEAL, "Cycle": NAVY, "Transit": OCHRE}


def apply_style():
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlepad": 16,
        "axes.labelsize": 10,
        "text.color": NAVY,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.edgecolor": "#D8E2E8",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.axisbelow": True,
        "grid.color": "#E8EEF2",
        "grid.linewidth": .8,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "svg.hashsalt": "hayiwei-data-viz-gallery",
        "svg.fonttype": "none",
    })
