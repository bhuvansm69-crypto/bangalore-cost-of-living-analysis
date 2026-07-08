"""
data.py
Data loading, cleaning, filtering, and derived-metric calculations for the
Bangalore Cost of Living dashboard. All functions are pure (take data in,
return data out) so they're easy to test and reuse inside Dash callbacks.
"""

from __future__ import annotations

import sqlite3
from functools import lru_cache
from typing import Optional

import numpy as np
import pandas as pd

from dashboard.config import DATA_PATH, DB_PATH, COST_CATEGORIES, LOCALITY_COORDS


# ------------------------------------------------------------------
# Loading & cleaning
# ------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    """
    Load and clean the raw dataset once per process (cached).
    Returns a DataFrame with normalized column names and derived time fields.
    """
    df = pd.read_csv(DATA_PATH)

    df = df.rename(columns={
        "Timestamp": "timestamp",
        "Locality": "locality",
        "Category": "category",
        "Item_or_Route": "item",
        "Provider": "provider",
        "Price_INR": "price",
        "DayType": "day_type",
        "Weather": "weather",
        "Demand": "demand",
        "Notes": "notes",
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    df = df[df["price"] > 0]

    for col in ["locality", "category", "item", "provider", "day_type", "weather", "demand"]:
        df[col] = df[col].astype(str).str.strip()
    df["category"] = df["category"].str.lower()

    df["month"] = df["timestamp"].dt.to_period("M").astype(str)
    df["year"] = df["timestamp"].dt.year
    df["date"] = df["timestamp"].dt.date

    df = df.drop_duplicates()

    # Attach lat/lon for map visualizations
    df["lat"] = df["locality"].map(lambda l: LOCALITY_COORDS.get(l, (None, None))[0])
    df["lon"] = df["locality"].map(lambda l: LOCALITY_COORDS.get(l, (None, None))[1])

    return df


def build_sqlite(df: Optional[pd.DataFrame] = None) -> None:
    """Persist the cleaned dataframe into a SQLite database for SQL-based access."""
    if df is None:
        df = load_data()
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("costs", conn, if_exists="replace", index=False)
    conn.close()


# ------------------------------------------------------------------
# Filtering
# ------------------------------------------------------------------

def filter_data(
    df: pd.DataFrame,
    localities: Optional[list] = None,
    categories: Optional[list] = None,
    providers: Optional[list] = None,
    date_range: Optional[tuple] = None,
    price_range: Optional[tuple] = None,
    search: Optional[str] = None,
) -> pd.DataFrame:
    """Apply all active filters to the dataset. Any None/empty filter is skipped."""
    out = df

    if localities:
        out = out[out["locality"].isin(localities)]
    if categories:
        out = out[out["category"].isin(categories)]
    if providers:
        out = out[out["provider"].isin(providers)]
    if date_range and date_range[0] and date_range[1]:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        out = out[(out["timestamp"] >= start) & (out["timestamp"] <= end)]
    if price_range:
        lo, hi = price_range
        out = out[(out["price"] >= lo) & (out["price"] <= hi)]
    if search:
        s = search.strip().lower()
        if s:
            mask = (
                out["locality"].str.lower().str.contains(s)
                | out["category"].str.lower().str.contains(s)
                | out["provider"].str.lower().str.contains(s)
                | out["item"].str.lower().str.contains(s)
            )
            out = out[mask]

    return out


# ------------------------------------------------------------------
# KPIs
# ------------------------------------------------------------------

def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute the top-line KPI numbers shown as cards on the dashboard."""
    if df.empty:
        return {
            "total_records": 0, "total_localities": 0, "total_categories": 0,
            "total_providers": 0, "avg_cost": 0, "avg_rent": 0, "avg_grocery": 0,
            "avg_delivery": 0, "max_cost": 0, "min_cost": 0, "cost_index": 0,
        }

    def cat_avg(cat):
        sub = df[df["category"] == cat]["price"]
        return round(sub.mean(), 2) if len(sub) else 0.0

    return {
        "total_records": len(df),
        "total_localities": df["locality"].nunique(),
        "total_categories": df["category"].nunique(),
        "total_providers": df["provider"].nunique(),
        "avg_cost": round(df["price"].mean(), 2),
        "avg_rent": cat_avg("rent"),
        "avg_grocery": cat_avg("grocery"),
        "avg_delivery": cat_avg("delivery_app"),
        "max_cost": round(df["price"].max(), 2),
        "min_cost": round(df["price"].min(), 2),
        "cost_index": round(cost_of_living_index(df)["index"].mean(), 2) if len(df) else 0,
    }


# ------------------------------------------------------------------
# Analytics: Cost of Living Index & rankings
# ------------------------------------------------------------------

def cost_of_living_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a per-locality Cost of Living Index.

    Method: for each category, min-max normalize the locality's average price
    to a 0-100 scale, then average across categories present in the data.
    This keeps the index interpretable (0 = cheapest observed, 100 = most
    expensive observed) and robust to categories with very different price
    scales (e.g., rent in thousands vs bmtc fare in tens).
    """
    if df.empty:
        return pd.DataFrame(columns=["locality", "index"])

    pivot = df.pivot_table(index="locality", columns="category", values="price", aggfunc="mean")

    # Vectorized min-max normalization per column (avoids DataFrame.apply, which
    # can silently collapse to a Series when the pivot has only one column —
    # e.g. when the user filters down to a single category).
    col_min = pivot.min(axis=0)
    col_max = pivot.max(axis=0)
    col_range = (col_max - col_min).replace(0, pd.NA)
    normalized = (pivot - col_min) / col_range * 100
    normalized = normalized.fillna(50.0)  # constant-price columns get a neutral midpoint score

    result = normalized.mean(axis=1).reset_index()
    result.columns = ["locality", "index"]
    return result.sort_values("index", ascending=False).reset_index(drop=True)


def affordability_score(df: pd.DataFrame) -> pd.DataFrame:
    """Inverse of the cost index (100 - index): higher score = more affordable."""
    coi = cost_of_living_index(df)
    coi["affordability_score"] = 100 - coi["index"]
    return coi


def provider_ranking(df: pd.DataFrame, category: Optional[str] = None) -> pd.DataFrame:
    """Rank providers by average price, optionally scoped to one category."""
    sub = df if category is None else df[df["category"] == category]
    if sub.empty:
        return pd.DataFrame(columns=["provider", "avg_price", "n"])
    out = (
        sub.groupby("provider")["price"]
        .agg(avg_price="mean", n="count")
        .reset_index()
        .sort_values("avg_price", ascending=False)
    )
    out["avg_price"] = out["avg_price"].round(2)
    return out


def monthly_insights(df: pd.DataFrame) -> pd.DataFrame:
    """Average price trend by month, overall."""
    if df.empty:
        return pd.DataFrame(columns=["month", "avg_price"])
    out = df.groupby("month")["price"].mean().reset_index()
    out.columns = ["month", "avg_price"]
    out["avg_price"] = out["avg_price"].round(2)
    return out.sort_values("month")


def generate_insights(df: pd.DataFrame) -> list:
    """
    Produce a short list of automatic, plain-English insights from the
    currently filtered data. Used in the 'Analytics' page insight cards.
    """
    insights = []
    if df.empty:
        return ["No data matches the current filters."]

    coi = cost_of_living_index(df)
    if len(coi) >= 2:
        most = coi.iloc[0]
        least = coi.iloc[-1]
        insights.append(
            f"{most['locality']} is currently the most expensive locality overall "
            f"(index {most['index']:.0f}/100), while {least['locality']} is the most "
            f"affordable (index {least['index']:.0f}/100)."
        )

    if "rent" in df["category"].values:
        rent = df[df["category"] == "rent"].groupby("locality")["price"].mean()
        if len(rent) >= 2:
            spread_pct = (rent.max() - rent.min()) / rent.min() * 100
            insights.append(
                f"Rent varies by about {spread_pct:.0f}% between the cheapest and most "
                f"expensive locality in the current selection."
            )

    trend = monthly_insights(df)
    if len(trend) >= 2:
        change = trend["avg_price"].iloc[-1] - trend["avg_price"].iloc[0]
        direction = "risen" if change > 0 else "fallen"
        insights.append(
            f"Average prices have {direction} by ₹{abs(change):.0f} from "
            f"{trend['month'].iloc[0]} to {trend['month'].iloc[-1]} in the current selection."
        )

    if "provider" in df.columns and df["category"].isin(["delivery_app"]).any():
        prov = provider_ranking(df, "delivery_app")
        if len(prov) >= 2:
            insights.append(
                f"Among food delivery providers, {prov.iloc[0]['provider']} has the highest "
                f"average price (₹{prov.iloc[0]['avg_price']:.0f}) while "
                f"{prov.iloc[-1]['provider']} is cheapest on average "
                f"(₹{prov.iloc[-1]['avg_price']:.0f})."
            )

    return insights


def top_recommendations(df: pd.DataFrame, n: int = 3) -> list:
    """Return the top-N most affordable localities as a simple recommendation list."""
    coi = affordability_score(df)
    if coi.empty:
        return []
    top = coi.sort_values("affordability_score", ascending=False).head(n)
    return [
        f"{row.locality} — affordability score {row.affordability_score:.0f}/100"
        for row in top.itertuples()
    ]
