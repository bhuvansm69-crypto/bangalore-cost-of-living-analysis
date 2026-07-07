"""
advanced_visualize.py
Generates advanced, interactive visualizations for the Bangalore Cost Tracker
dataset — designed to reveal multi-dimensional patterns (locality x category x
provider x time) that simple bar/pie charts can't show.

Chart types included, and why each one earns its place:
  1. Sunburst          -> Locality -> Category -> Provider hierarchy in one view
  2. Treemap           -> proportional cost weight per locality/category at a glance
  3. Heatmap           -> Locality x Category price matrix, spot patterns instantly
  4. Animated bar race -> rent evolving month by month, locality by locality
  5. Radar chart        -> compare 5 localities across all categories simultaneously
  6. Violin + box       -> full price distribution per category, not just the average
  7. Parallel categories-> trace how localities flow across price tiers per category
  8. 3D scatter          -> locality x month x price, colored by category
  9. Combined dashboard  -> all key views stitched into a single scrollable HTML page

All charts are saved as standalone interactive HTML (open in any browser, or embed
in a GitHub Pages / portfolio site). PNG snapshots are also saved for slides/README
embedding, via kaleido.
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------------
# Config
# -------------------------------
DATA_PATH = "data/processed/bangalore_cost_tracker_clean.csv"
HTML_DIR = "reports/interactive"
PNG_DIR = "reports/figures"

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

print("=" * 70)
print("GENERATING ADVANCED VISUALIZATIONS")
print("=" * 70)


def save_chart(fig, name, height=750, width=1300):
    """Save every chart as both interactive HTML and a static PNG snapshot."""
    html_path = os.path.join(HTML_DIR, f"{name}.html")
    png_path = os.path.join(PNG_DIR, f"{name}.png")
    # include_plotlyjs="cdn" keeps each file small (~15KB instead of ~4.7MB)
    # by loading the Plotly library from a CDN instead of bundling it every time.
    # Requires internet access when the HTML is opened.
    fig.write_html(html_path, include_plotlyjs="cdn")

    try:
        fig.write_image(png_path, width=width, height=height, scale=2)
    except Exception as e:
        print(f"  (PNG export skipped for {name}: {e})")
    print(f"Saved: {name}  [html + png]")


# -------------------------------
# Load & prep data
# -------------------------------
df = pd.read_csv(DATA_PATH)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Month"] = df["Timestamp"].dt.to_period("M").astype(str)


# ==========================================================
# 1. SUNBURST — Locality -> Category -> Provider
# ==========================================================
sunburst_df = (
    df.groupby(["Locality", "Category", "Provider"])["Price_INR"]
    .mean()
    .reset_index()
)

fig = px.sunburst(
    sunburst_df,
    path=["Locality", "Category", "Provider"],
    values="Price_INR",
    color="Price_INR",
    color_continuous_scale="RdYlGn_r",
    title="Cost Breakdown: Locality → Category → Provider (click to zoom in)",
)
fig.update_layout(template="plotly_white", margin=dict(t=60, l=0, r=0, b=0))
save_chart(fig, "01_sunburst_locality_category_provider", height=900)


# ==========================================================
# 2. TREEMAP — proportional cost weight
# ==========================================================
treemap_df = (
    df.groupby(["Category", "Locality"])["Price_INR"]
    .mean()
    .reset_index()
)

fig = px.treemap(
    treemap_df,
    path=["Category", "Locality"],
    values="Price_INR",
    color="Price_INR",
    color_continuous_scale="Blues",
    title="Cost Weight by Category and Locality (box size = relative price)",
)
fig.update_layout(template="plotly_white", margin=dict(t=60, l=0, r=0, b=0))
save_chart(fig, "02_treemap_category_locality", height=800)


# ==========================================================
# 3. HEATMAP — Locality x Category price matrix
# ==========================================================
pivot = df.pivot_table(index="Locality", columns="Category", values="Price_INR", aggfunc="mean")
# Normalize each category column to 0-1 so categories with very different price
# scales (rent vs auto fare) are visually comparable on the same heatmap
pivot_norm = (pivot - pivot.min()) / (pivot.max() - pivot.min())

fig = px.imshow(
    pivot_norm,
    color_continuous_scale="RdYlGn_r",
    aspect="auto",
    title="Relative Price Intensity Heatmap (normalized 0–1 per category)",
    labels=dict(color="Relative Price"),
)
fig.update_layout(template="plotly_white", xaxis_title="Category", yaxis_title="Locality")
save_chart(fig, "03_heatmap_locality_category", height=900)


# ==========================================================
# 4. ANIMATED BAR CHART RACE — rent by locality, month by month
# ==========================================================
rent_monthly = (
    df[df["Category"] == "rent"]
    .groupby(["Month", "Locality"])["Price_INR"]
    .mean()
    .reset_index()
)
# Rank within each month so the race shows position changes clearly
rent_monthly["rank"] = rent_monthly.groupby("Month")["Price_INR"].rank(ascending=False)
rent_monthly = rent_monthly[rent_monthly["rank"] <= 15]  # top 15 keeps it readable

fig = px.bar(
    rent_monthly.sort_values(["Month", "Price_INR"]),
    x="Price_INR",
    y="Locality",
    color="Locality",
    animation_frame="Month",
    orientation="h",
    range_x=[0, rent_monthly["Price_INR"].max() * 1.1],
    title="Rent by Locality Over Time — Top 15 (press play)",
)
fig.update_layout(template="plotly_white", showlegend=False)
save_chart(fig, "04_animated_rent_race", height=800)


# ==========================================================
# 5. RADAR CHART — compare 5 localities across all categories
# ==========================================================
top_localities = df.groupby("Locality")["Price_INR"].mean().sort_values(ascending=False).head(5).index.tolist()

radar_df = (
    df[df["Locality"].isin(top_localities)]
    .groupby(["Locality", "Category"])["Price_INR"]
    .mean()
    .reset_index()
)
# Normalize per category (0-1) so categories with different scales plot sensibly together
cat_min = df.groupby("Category")["Price_INR"].min()
cat_max = df.groupby("Category")["Price_INR"].max()
radar_df["norm_price"] = radar_df.apply(
    lambda r: (r["Price_INR"] - cat_min[r["Category"]]) / (cat_max[r["Category"]] - cat_min[r["Category"]]),
    axis=1,
)

fig = go.Figure()
categories = sorted(radar_df["Category"].unique())
for loc in top_localities:
    sub = radar_df[radar_df["Locality"] == loc].set_index("Category").reindex(categories)
    fig.add_trace(go.Scatterpolar(
        r=sub["norm_price"].tolist() + [sub["norm_price"].tolist()[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=loc,
    ))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    title="Top 5 Most Expensive Localities — Category Profile Comparison (normalized)",
    template="plotly_white",
)
save_chart(fig, "05_radar_top5_localities", height=800)


# ==========================================================
# 6. VIOLIN + BOX — full price distribution per category
# ==========================================================
fig = go.Figure()
for cat in sorted(df["Category"].unique()):
    fig.add_trace(go.Violin(
        y=df[df["Category"] == cat]["Price_INR"],
        name=cat,
        box_visible=True,
        meanline_visible=True,
        points=False,
    ))
fig.update_layout(
    title="Full Price Distribution per Category (violin + box, not just averages)",
    template="plotly_white",
    yaxis_title="Price (₹)",
)
save_chart(fig, "06_violin_category_distribution", height=800)


# ==========================================================
# 7. PARALLEL CATEGORIES — how localities flow across price tiers
# ==========================================================
tier_df = df.pivot_table(index="Locality", columns="Category", values="Price_INR", aggfunc="mean")
def tier_label(series, n=3):
    return pd.qcut(series, n, labels=["Low", "Mid", "High"])
tier_labels = tier_df.apply(tier_label)
tier_labels = tier_labels.reset_index()

# Build a plain numeric color array (avoid passing a categorical Series tied to
# a column name plotly might try to reconcile against the source dataframe)
color_col = "rent" if "rent" in tier_labels.columns else tier_labels.columns[1]
color_values = tier_labels[color_col].map({"Low": 0, "Mid": 1, "High": 2}).astype(float).to_numpy()

fig = px.parallel_categories(
    tier_labels,
    dimensions=[c for c in tier_labels.columns if c != "Locality"],
    color=color_values,
    color_continuous_scale=px.colors.sequential.Sunset,
    title="Locality Price Tiers Across Categories (Low/Mid/High) — trace the flows",
)
fig.update_layout(template="plotly_white")
save_chart(fig, "07_parallel_categories_tiers", height=800)


# ==========================================================
# 8. 3D SCATTER — Locality x Month x Price, colored by Category
# ==========================================================
scatter_df = (
    df.groupby(["Locality", "Month", "Category"])["Price_INR"]
    .mean()
    .reset_index()
)
locality_order = {loc: i for i, loc in enumerate(sorted(scatter_df["Locality"].unique()))}
scatter_df["locality_idx"] = scatter_df["Locality"].map(locality_order)
month_order = {m: i for i, m in enumerate(sorted(scatter_df["Month"].unique()))}
scatter_df["month_idx"] = scatter_df["Month"].map(month_order)

fig = px.scatter_3d(
    scatter_df,
    x="locality_idx",
    y="month_idx",
    z="Price_INR",
    color="Category",
    hover_data=["Locality", "Month"],
    title="3D View: Locality × Month × Price, by Category",
)
fig.update_layout(
    template="plotly_white",
    scene=dict(
        xaxis_title="Locality (indexed)",
        yaxis_title="Month (indexed)",
        zaxis_title="Price (₹)",
    ),
)
save_chart(fig, "08_3d_scatter_locality_month_price", height=900)


# ==========================================================
# 9. COMBINED DASHBOARD — top expensive/cheap + category avg + trend, one page
# ==========================================================
top10 = df.groupby("Locality")["Price_INR"].mean().sort_values(ascending=False).head(10).reset_index()
cheap10 = df.groupby("Locality")["Price_INR"].mean().sort_values().head(10).reset_index()
cat_avg = df.groupby("Category")["Price_INR"].mean().reset_index()
monthly_trend = df.groupby("Month")["Price_INR"].mean().reset_index()

dash = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Top 10 Most Expensive Localities (overall avg)",
        "Top 10 Most Affordable Localities (overall avg)",
        "Average Price by Category",
        "Overall Monthly Price Trend",
    ),
    specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "scatter"}]],
)

dash.add_trace(go.Bar(x=top10["Locality"], y=top10["Price_INR"], marker_color="crimson", showlegend=False), row=1, col=1)
dash.add_trace(go.Bar(x=cheap10["Locality"], y=cheap10["Price_INR"], marker_color="seagreen", showlegend=False), row=1, col=2)
dash.add_trace(go.Bar(x=cat_avg["Category"], y=cat_avg["Price_INR"], marker_color="steelblue", showlegend=False), row=2, col=1)
dash.add_trace(go.Scatter(x=monthly_trend["Month"], y=monthly_trend["Price_INR"], mode="lines+markers", line_color="darkorange", showlegend=False), row=2, col=2)

dash.update_xaxes(tickangle=-45, row=1, col=1)
dash.update_xaxes(tickangle=-45, row=1, col=2)
dash.update_xaxes(tickangle=-45, row=2, col=1)

dash.update_layout(
    title_text="Bangalore Cost of Living — Overview Dashboard",
    template="plotly_white",
    height=900,
    width=1500,
)
save_chart(dash, "09_combined_dashboard", height=900, width=1500)


print("\nAll advanced charts generated successfully!")
print(f"Interactive HTML files -> {HTML_DIR}/")
print(f"Static PNG snapshots   -> {PNG_DIR}/")