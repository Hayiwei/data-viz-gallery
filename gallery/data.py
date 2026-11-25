"""Deterministic synthetic data. No external data or real observations."""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 2026


def generate_data() -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    dates = pd.date_range("2026-01-01", periods=90)
    weekends = dates.dayofweek >= 5
    daily = pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"),
        "trips": np.maximum(0, np.round(170 + 24 * np.sin(np.arange(90) / 12) - 45 * weekends + rng.normal(0, 12, 90))).astype(int),
    })
    mode = np.repeat(["Walk", "Cycle", "Transit"], 120)
    distance = np.concatenate([
        rng.uniform(.3, 3.5, 120), rng.uniform(1, 10, 120), rng.uniform(2, 22, 120),
    ])
    duration = np.concatenate([
        distance[:120] / 4.5 * 60 + rng.normal(0, 2, 120),
        distance[120:240] / 15 * 60 + rng.normal(0, 3, 120),
        distance[240:] / 28 * 60 + 9 + rng.normal(0, 5, 120),
    ])
    commutes = pd.DataFrame({
        "mode": mode, "distance_km": np.round(distance, 2),
        "duration_min": np.round(np.maximum(1, duration), 1),
    })
    category_means = {"Groceries": 330, "Dining": 185, "Transport": 105, "Learning": 75, "Leisure": 125}
    spending = pd.DataFrame([
        {"month": month, "category": category, "amount_cu": round(max(0, mean + rng.normal(0, mean * .12)), 2)}
        for month in range(1, 13) for category, mean in category_means.items()
    ])
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    activity = pd.DataFrame([
        {
            "weekday": day, "hour": hour,
            "events": int(max(0, round(
                8 + 37 * np.exp(-((hour - 9) / 2.6) ** 2)
                + 48 * np.exp(-((hour - 18) / 3.2) ** 2)
                - (12 if day in ["Sat", "Sun"] else 0) + rng.normal(0, 3)
            ))),
        }
        for day in weekdays for hour in range(24)
    ])
    return {"daily_trips": daily, "commutes": commutes, "spending": spending, "activity": activity}


def write_data(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name, data in generate_data().items():
        data.to_csv(destination / f"{name}.csv", index=False)


def read_data(source: Path) -> dict[str, pd.DataFrame]:
    return {name: pd.read_csv(source / f"{name}.csv") for name in ("daily_trips", "commutes", "spending", "activity")}
