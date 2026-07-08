# Bangalore Cost of Living Dashboard

An interactive Dash web application analyzing cost-of-living data across 50 Bangalore localities, 10 spending categories, and 18 service providers — 100,000 records total.

> **Data note:** the dataset is synthetic (AI-generated to simulate realistic price patterns) and is used here to demonstrate a complete analytics + dashboarding pipeline at city scale. See the "About" page in the app for details.

---

## Features

- **7 pages**: Dashboard, Analytics, Locality Explorer, Provider Comparison, Map, Raw Data, About
- **Light/Dark theme toggle** with instant, client-side switching (no page reload)
- **Collapsible sidebar** navigation
- **11 KPI cards**: total records, localities, categories, providers, average/min/max costs, and a composite Cost of Living Index
- **Full filter panel** on every page: locality, category, provider, free-text search, date range, and price range — all charts update automatically
- **24 chart types** across the app: bar, grouped bar, stacked bar, line, area, histogram, box, violin, pie, treemap, sunburst, heatmap, correlation matrix, radar, scatter, bubble, and an interactive Mapbox locality map
- **Automatic insights**: plain-English findings generated from whatever is currently filtered (e.g. "Rent varies by ~28% between the cheapest and most expensive locality in the current selection")
- **Data table** with sorting, native filtering, pagination, and CSV export of the currently filtered data

## Architecture

```
dashboard/
├── app.py            # Entry point: Dash app init, layout shell, run server
├── config.py          # Paths, color themes, locality coordinates, category labels
├── data.py            # Load/clean data, filtering, KPI + analytics calculations
├── theme.py            # Light/dark Plotly styling helper
├── components.py      # Reusable UI: KPI cards, sidebar, filter panel, chart cards
├── charts.py            # All chart-generating functions (pure: df + theme -> figure)
├── layouts.py          # Page layouts (one function per route)
├── callbacks.py        # All interactivity: routing, filters, theme, export
├── utils.py            # Small formatting helpers
└── assets/
    └── style.css        # Glassmorphism styling, responsive layout, theme variables
```

Design principles used throughout:
- **Pure functions** in `charts.py` and `data.py` — same input always gives same output, easy to test independently of the running app (see `tests/` if you add any)
- **Cached data loading** — the dataset is read and cleaned once per process, not on every callback
- **Shared filter component IDs across pages** — since only one page is mounted in the DOM at a time, this avoids duplicating filter logic seven times

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
python dashboard/app.py
```

Then open **http://127.0.0.1:8050** in your browser.

## Dependencies

- Python 3.10+
- Dash, Dash Bootstrap Components
- Plotly
- Pandas, NumPy
- openpyxl (for reading the source Excel dataset)

## Future Improvements

- Replace synthetic data with real collected prices for validation
- Add a simple regression model to predict rent from other locality features
- Server-side caching (e.g. Flask-Caching) for the filtered-dataframe computation if deployed with concurrent users
- Add unit tests under `tests/` covering `data.py` and `charts.py` directly (all functions are already structured to support this)
