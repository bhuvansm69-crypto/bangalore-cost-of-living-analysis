import os
import pandas as pd
import plotly.express as px

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("data/processed/bangalore_cost_tracker_clean.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Month"] = df["Timestamp"].dt.to_period("M").astype(str)

OUTPUT = "dashboard"

os.makedirs(OUTPUT, exist_ok=True)


def save_dashboard(fig, filename):
    path = os.path.join(OUTPUT, filename)
    fig.write_html(path)
    print(f"Saved -> {filename}")


# =====================================================
# Dashboard 1
# Top 10 Expensive Localities
# =====================================================

top10 = (
    df.groupby("Locality")["Price_INR"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top10,
    x="Locality",
    y="Price_INR",
    title="Top 10 Most Expensive Localities",
    text_auto=".2f"
)

save_dashboard(fig, "01_top10_expensive_localities.html")


# =====================================================
# Dashboard 2
# Cheapest Localities
# =====================================================

cheap = (
    df.groupby("Locality")["Price_INR"]
    .mean()
    .sort_values()
    .head(10)
    .reset_index()
)

fig = px.bar(
    cheap,
    x="Locality",
    y="Price_INR",
    title="Top 10 Affordable Localities",
    text_auto=".2f"
)

save_dashboard(fig, "02_affordable_localities.html")


# =====================================================
# Dashboard 3
# Category Comparison
# =====================================================

category = (
    df.groupby("Category")["Price_INR"]
    .mean()
    .reset_index()
)

fig = px.bar(
    category,
    x="Category",
    y="Price_INR",
    title="Average Cost by Category",
    color="Category"
)

save_dashboard(fig, "03_category_comparison.html")


# =====================================================
# Dashboard 4
# Provider Comparison
# =====================================================

provider = (
    df.groupby("Provider")["Price_INR"]
    .mean()
    .reset_index()
)

fig = px.bar(
    provider,
    x="Provider",
    y="Price_INR",
    color="Provider",
    title="Average Cost by Provider"
)

save_dashboard(fig, "04_provider_comparison.html")


# =====================================================
# Dashboard 5
# Monthly Trend
# =====================================================

monthly = (
    df.groupby("Month")["Price_INR"]
    .mean()
    .reset_index()
)

fig = px.line(
    monthly,
    x="Month",
    y="Price_INR",
    markers=True,
    title="Monthly Average Cost Trend"
)

save_dashboard(fig, "05_monthly_trend.html")


# =====================================================
# Dashboard 6
# Rent Comparison
# =====================================================

rent = (
    df[df["Category"] == "rent"]
    .groupby("Locality")["Price_INR"]
    .mean()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)

fig = px.bar(
    rent,
    x="Locality",
    y="Price_INR",
    title="Average Rent by Locality"
)

save_dashboard(fig, "06_rent_comparison.html")


# =====================================================
# Dashboard 7
# Price Distribution
# =====================================================

fig = px.histogram(
    df,
    x="Price_INR",
    nbins=50,
    title="Distribution of Prices"
)

save_dashboard(fig, "07_price_distribution.html")


# =====================================================
# Dashboard 8
# Category Pie Chart
# =====================================================

fig = px.pie(
    df,
    names="Category",
    title="Category Distribution"
)

save_dashboard(fig, "08_category_distribution.html")


# =====================================================
# Dashboard 9
# Box Plot
# =====================================================

fig = px.box(
    df,
    x="Category",
    y="Price_INR",
    title="Price Distribution by Category"
)

save_dashboard(fig, "09_boxplot.html")


# =====================================================
# Dashboard 10
# Treemap
# =====================================================

tree = (
    df.groupby(["Category", "Provider"])["Price_INR"]
    .mean()
    .reset_index()
)

fig = px.treemap(
    tree,
    path=["Category", "Provider"],
    values="Price_INR",
    title="Category → Provider Cost Treemap"
)

save_dashboard(fig, "10_treemap.html")

print("\n")
print("="*60)
print("ALL DASHBOARDS CREATED SUCCESSFULLY")
print("="*60)