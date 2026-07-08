"""
charts.py
All chart-generating functions. Each function takes the (already filtered)
dataframe and the current theme mode, and returns a ready-to-render Plotly
figure. Keeping these as pure functions makes callbacks.py simple: it just
calls the right function and passes the result to a dcc.Graph.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import CATEGORY_LABELS, CHART_COLOR_SEQUENCE
from theme import style_figure
from data import cost_of_living_index, monthly_insights


def _empty_fig(mode: str, message: str = "No data for current filters"):
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, font=dict(size=14))
    return style_figure(fig, mode)


# ------------------------------------------------------------------
# Locality rankings
# ------------------------------------------------------------------

def top_expensive_localities(df: pd.DataFrame, mode: str, n: int = 10):
    if df.empty:
        return _empty_fig(mode)
    top = df.groupby("locality")["price"].mean().sort_values(ascending=False).head(n).reset_index()
    fig = px.bar(top, x="locality", y="price", title=f"Top {n} Most Expensive Localities",
                 labels={"price": "Avg Price (₹)", "locality": ""})
    fig.update_xaxes(tickangle=-40)
    return style_figure(fig, mode)


def top_affordable_localities(df: pd.DataFrame, mode: str, n: int = 10):
    if df.empty:
        return _empty_fig(mode)
    bottom = df.groupby("locality")["price"].mean().sort_values().head(n).reset_index()
    fig = px.bar(bottom, x="locality", y="price", title=f"Top {n} Most Affordable Localities",
                 labels={"price": "Avg Price (₹)", "locality": ""},
                 color_discrete_sequence=["#22c55e"])
    fig.update_xaxes(tickangle=-40)
    return style_figure(fig, mode)


def top5_vs_bottom5(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    coi = cost_of_living_index(df)
    if len(coi) < 2:
        return _empty_fig(mode)
    top5 = coi.head(5).copy(); top5["group"] = "Most Expensive"
    bottom5 = coi.tail(5).copy(); bottom5["group"] = "Most Affordable"
    combined = pd.concat([top5, bottom5])
    fig = px.bar(combined, x="locality", y="index", color="group", barmode="group",
                 title="Top 5 vs Bottom 5 Localities (Cost of Living Index)",
                 labels={"index": "Cost Index (0-100)", "locality": ""},
                 color_discrete_map={"Most Expensive": "#ef4444", "Most Affordable": "#22c55e"})
    fig.update_xaxes(tickangle=-30)
    return style_figure(fig, mode)


def cost_index_ranking(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    coi = cost_of_living_index(df)
    fig = px.bar(coi, x="index", y="locality", orientation="h",
                 title="Cost of Living Index — Full Ranking",
                 labels={"index": "Index (0-100)", "locality": ""},
                 color="index", color_continuous_scale="RdYlGn_r")
    fig.update_layout(height=900, yaxis=dict(categoryorder="total ascending"))
    return style_figure(fig, mode)


# ------------------------------------------------------------------
# Category-level views
# ------------------------------------------------------------------

def category_average_bar(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    cat = df.groupby("category")["price"].mean().reset_index()
    cat["label"] = cat["category"].map(lambda c: CATEGORY_LABELS.get(c, c.title()))
    fig = px.bar(cat.sort_values("price", ascending=False), x="label", y="price",
                 title="Average Price by Category", labels={"price": "Avg Price (₹)", "label": ""})
    return style_figure(fig, mode)


def category_by_locality_bar(df: pd.DataFrame, mode: str, category: str, n: int = 15):
    sub = df[df["category"] == category]
    if sub.empty:
        return _empty_fig(mode, f"No data for {category}")
    top = sub.groupby("locality")["price"].mean().sort_values(ascending=False).head(n).reset_index()
    label = CATEGORY_LABELS.get(category, category.title())
    fig = px.bar(top, x="locality", y="price", title=f"Average {label} by Locality",
                 labels={"price": "Avg Price (₹)", "locality": ""})
    fig.update_xaxes(tickangle=-40)
    return style_figure(fig, mode)


def pie_category_share(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    fig = px.pie(df, names="category", title="Record Share by Category", hole=0.45)
    return style_figure(fig, mode)


def treemap_category_locality(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    t = df.groupby(["category", "locality"])["price"].mean().reset_index()
    fig = px.treemap(t, path=["category", "locality"], values="price", color="price",
                      color_continuous_scale="Blues", title="Cost Weight: Category → Locality")
    return style_figure(fig, mode)


def sunburst_locality_category_provider(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    s = df.groupby(["locality", "category", "provider"])["price"].mean().reset_index()
    fig = px.sunburst(s, path=["locality", "category", "provider"], values="price",
                       color="price", color_continuous_scale="RdYlGn_r",
                       title="Locality → Category → Provider Breakdown")
    return style_figure(fig, mode)


def heatmap_locality_category(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    pivot = df.pivot_table(index="locality", columns="category", values="price", aggfunc="mean")
    norm = (pivot - pivot.min()) / (pivot.max() - pivot.min())
    fig = px.imshow(norm, color_continuous_scale="RdYlGn_r", aspect="auto",
                     title="Relative Price Intensity (normalized per category)",
                     labels=dict(color="Relative Price"))
    fig.update_layout(height=800)
    return style_figure(fig, mode)


def correlation_matrix(df: pd.DataFrame, mode: str):
    """Correlation between category average prices, computed per locality."""
    if df.empty:
        return _empty_fig(mode)
    pivot = df.pivot_table(index="locality", columns="category", values="price", aggfunc="mean")
    if pivot.shape[1] < 2:
        return _empty_fig(mode, "Need at least 2 categories for a correlation matrix")
    corr = pivot.corr()
    corr.columns = [CATEGORY_LABELS.get(c, c) for c in corr.columns]
    corr.index = [CATEGORY_LABELS.get(c, c) for c in corr.index]
    fig = px.imshow(corr, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                     title="Correlation Between Category Prices (across localities)",
                     text_auto=".2f")
    return style_figure(fig, mode)


def radar_top_localities(df: pd.DataFrame, mode: str, n: int = 5):
    if df.empty:
        return _empty_fig(mode)
    top = df.groupby("locality")["price"].mean().sort_values(ascending=False).head(n).index.tolist()
    sub = df[df["locality"].isin(top)].groupby(["locality", "category"])["price"].mean().reset_index()
    cat_min = df.groupby("category")["price"].min()
    cat_max = df.groupby("category")["price"].max()
    sub["norm"] = sub.apply(
        lambda r: (r["price"] - cat_min[r["category"]]) / (cat_max[r["category"]] - cat_min[r["category"]])
        if cat_max[r["category"]] != cat_min[r["category"]] else 0.5, axis=1)

    categories = sorted(sub["category"].unique())
    fig = go.Figure()
    for loc in top:
        s = sub[sub["locality"] == loc].set_index("category").reindex(categories)
        vals = s["norm"].tolist()
        fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=categories + [categories[0]],
                                       fill="toself", name=loc))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                       title=f"Top {n} Localities — Category Profile (normalized)")
    return style_figure(fig, mode)


# ------------------------------------------------------------------
# Distributions
# ------------------------------------------------------------------

def price_histogram(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    fig = px.histogram(df, x="price", nbins=50, title="Price Distribution",
                        labels={"price": "Price (₹)"})
    return style_figure(fig, mode)


def price_box(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    fig = px.box(df, x="category", y="price", title="Price Distribution by Category",
                 labels={"price": "Price (₹)", "category": ""})
    return style_figure(fig, mode)


def price_violin(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    fig = go.Figure()
    for cat in sorted(df["category"].unique()):
        fig.add_trace(go.Violin(y=df[df["category"] == cat]["price"], name=cat,
                                 box_visible=True, meanline_visible=True, points=False))
    fig.update_layout(title="Full Price Distribution per Category")
    return style_figure(fig, mode)


# ------------------------------------------------------------------
# Time trends
# ------------------------------------------------------------------

def monthly_trend_line(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    m = monthly_insights(df)
    fig = px.line(m, x="month", y="avg_price", markers=True, title="Monthly Average Price Trend",
                   labels={"avg_price": "Avg Price (₹)", "month": ""})
    return style_figure(fig, mode)


def yearly_trend_bar(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    y = df.groupby("year")["price"].mean().reset_index()
    fig = px.bar(y, x="year", y="price", title="Yearly Average Price Trend",
                 labels={"price": "Avg Price (₹)", "year": ""})
    return style_figure(fig, mode)


def area_trend(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    m = df.groupby(["month", "category"])["price"].mean().reset_index()
    fig = px.area(m, x="month", y="price", color="category", title="Category Price Trend Over Time (stacked area)",
                  labels={"price": "Avg Price (₹)", "month": ""})
    return style_figure(fig, mode)


def stacked_bar_daytype(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    s = df.groupby(["category", "day_type"])["price"].mean().reset_index()
    fig = px.bar(s, x="category", y="price", color="day_type", barmode="group",
                 title="Weekday vs Weekend Price by Category",
                 labels={"price": "Avg Price (₹)", "category": ""})
    return style_figure(fig, mode)


# ------------------------------------------------------------------
# Provider comparisons
# ------------------------------------------------------------------

def provider_comparison_bar(df: pd.DataFrame, mode: str, category: str = None):
    sub = df if category is None else df[df["category"] == category]
    if sub.empty:
        return _empty_fig(mode)
    p = sub.groupby("provider")["price"].mean().reset_index().sort_values("price", ascending=False)
    title = "Provider Price Comparison" if category is None else f"Provider Comparison — {CATEGORY_LABELS.get(category, category)}"
    fig = px.bar(p, x="provider", y="price", title=title, labels={"price": "Avg Price (₹)", "provider": ""})
    return style_figure(fig, mode)


def head_to_head(df: pd.DataFrame, mode: str, provider_a: str, provider_b: str, category: str):
    sub = df[(df["category"] == category) & (df["provider"].isin([provider_a, provider_b]))]
    if sub.empty:
        return _empty_fig(mode, f"No data for {provider_a} vs {provider_b}")
    m = sub.groupby(["month", "provider"])["price"].mean().reset_index()
    fig = px.line(m, x="month", y="price", color="provider", markers=True,
                  title=f"{provider_a} vs {provider_b} — {CATEGORY_LABELS.get(category, category)}",
                  labels={"price": "Avg Price (₹)", "month": ""})
    return style_figure(fig, mode)


# ------------------------------------------------------------------
# Scatter / bubble
# ------------------------------------------------------------------

def scatter_price_by_demand(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    s = df.groupby(["locality", "demand"])["price"].mean().reset_index()
    fig = px.scatter(s, x="locality", y="price", color="demand", size="price",
                      title="Price by Locality, Sized & Colored by Demand Level",
                      labels={"price": "Avg Price (₹)", "locality": ""})
    fig.update_xaxes(tickangle=-40)
    return style_figure(fig, mode)


def bubble_category_provider(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    b = df.groupby(["category", "provider"])["price"].agg(["mean", "count"]).reset_index()
    b.columns = ["category", "provider", "avg_price", "count"]
    fig = px.scatter(b, x="category", y="avg_price", size="count", color="category",
                      hover_name="provider", title="Category vs Provider — Bubble Size = Record Count",
                      labels={"avg_price": "Avg Price (₹)", "category": ""})
    return style_figure(fig, mode)


# ------------------------------------------------------------------
# Map
# ------------------------------------------------------------------

def locality_map(df: pd.DataFrame, mode: str):
    if df.empty:
        return _empty_fig(mode)
    coi = cost_of_living_index(df)
    counts = df.groupby("locality").size().reset_index(name="records")
    coords = df[["locality", "lat", "lon"]].drop_duplicates()
    merged = coi.merge(coords, on="locality").merge(counts, on="locality")

    fig = px.scatter_mapbox(
        merged, lat="lat", lon="lon", color="index", size="records",
        hover_name="locality",
        hover_data={"index": ":.1f", "records": True, "lat": False, "lon": False},
        color_continuous_scale="RdYlGn_r",
        zoom=10, height=750,
        title="Bangalore Localities — Colored by Cost of Living Index",
    )
    fig.update_layout(mapbox_style="carto-darkmatter" if mode == "dark" else "carto-positron")
    fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
    return style_figure(fig, mode)
