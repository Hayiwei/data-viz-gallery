# Synthetic data provenance

All files are generated locally by gallery/data.py using NumPy seed 2026.
They contain no real observations and require no external source.

| File | Rows | Columns and units |
| --- | ---: | --- |
| daily_trips.csv | 90 | date (ISO date), trips (integer count per day) |
| commutes.csv | 360 | mode, distance_km (km), duration_min (minutes) |
| spending.csv | 60 | month (1–12), category, amount_cu (arbitrary currency units) |
| activity.csv | 168 | weekday (Mon–Sun), hour (0–23), events (integer count) |

- Daily trips combine a smooth oscillation, a weekend offset, and random noise.
- Commutes have 120 observations per mode. Walking, cycling, and transit use
  different sampled distances and assumed speeds. Transit adds a fixed waiting
  component. Durations include noise and are bounded below by one minute.
- Spending contains twelve generated months for each of five categories.
- Activity contains one count per weekday-hour cell, with two modeled daily
  peaks and lower weekend counts.

The patterns are designed for chart demonstrations. They are not empirical
evidence of behavior or differences between groups.

Regenerate: python -m gallery.build --regenerate-data
