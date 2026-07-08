"""
layouts.py
Page layouts for every sidebar route. Each function returns the page content
only (sidebar/topbar live in app.py's shared shell). Callbacks in
callbacks.py fill in chart data based on active filters.
"""

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

from components import kpi_row, filter_panel, chart_card
from config import CATEGORY_LABELS


def dashboard_layout(df):
    return html.Div(
        [
            filter_panel(df),
            kpi_row(),
            dbc.Row(
                [
                    chart_card("Top 10 Most Expensive Localities", "chart-top-expensive", md=6),
                    chart_card("Top 10 Most Affordable Localities", "chart-top-affordable", md=6),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Average Price by Category", "chart-category-avg", md=6),
                    chart_card("Monthly Average Price Trend", "chart-monthly-trend", md=6),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Cost Breakdown — Locality → Category → Provider", "chart-sunburst", md=12),
                ]
            ),
        ],
        className="page-content",
    )


def analytics_layout(df):
    return html.Div(
        [
            filter_panel(df),
            html.Div(id="insights-container", className="insights-row mb-3"),
            dbc.Row(
                [
                    chart_card("Cost of Living Index — Full Ranking", "chart-cost-index", md=6),
                    chart_card("Top 5 vs Bottom 5 Localities", "chart-top5-bottom5", md=6),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Price Distribution (Histogram)", "chart-histogram", md=4),
                    chart_card("Price Distribution by Category (Box)", "chart-box", md=4),
                    chart_card("Full Distribution (Violin)", "chart-violin", md=4),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Correlation Between Category Prices", "chart-correlation", md=6),
                    chart_card("Weekday vs Weekend Pricing", "chart-daytype", md=6),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Yearly Average Price Trend", "chart-yearly", md=6),
                    chart_card("Category Price Trend (Stacked Area)", "chart-area", md=6),
                ]
            ),
        ],
        className="page-content",
    )


def locality_layout(df):
    return html.Div(
        [
            filter_panel(df),
            dbc.Row(
                [
                    chart_card("Relative Price Intensity Heatmap", "chart-heatmap", md=12),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Top Localities — Category Profile (Radar)", "chart-radar", md=6),
                    chart_card("Cost Weight: Category → Locality (Treemap)", "chart-treemap", md=6),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Price by Locality, Colored by Demand", "chart-scatter-demand", md=12),
                ]
            ),
        ],
        className="page-content",
    )


def providers_layout(df):
    categories = sorted(df["category"].unique())
    return html.Div(
        [
            filter_panel(df),
            dbc.Row(
                [
                    dbc.Col([
                        html.Label("Compare category:", className="filter-label"),
                        dcc.Dropdown(
                            id="provider-category-select",
                            options=[{"label": CATEGORY_LABELS.get(c, c.title()), "value": c} for c in categories],
                            value="delivery_app" if "delivery_app" in categories else categories[0],
                            clearable=False,
                        ),
                    ], md=4, className="mb-3"),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Provider Comparison (selected category)", "chart-provider-bar", md=6),
                    chart_card("Category vs Provider (Bubble)", "chart-bubble", md=6),
                ]
            ),
            dbc.Row(
                [
                    chart_card("Swiggy vs Zomato — Monthly Trend", "chart-swiggy-zomato", md=6),
                    chart_card("Ola vs Uber — Monthly Trend", "chart-ola-uber", md=6),
                ]
            ),
        ],
        className="page-content",
    )


def map_layout(df):
    return html.Div(
        [
            filter_panel(df),
            dbc.Row(
                [
                    chart_card("Bangalore Localities Map", "chart-map", md=12),
                ]
            ),
        ],
        className="page-content",
    )


def data_layout(df):
    columns = ["timestamp", "locality", "category", "item", "provider", "price", "day_type", "weather", "demand"]
    return html.Div(
        [
            filter_panel(df),
            html.Div(
                [
                    dbc.Button(
                        [html.I(className="bi bi-download me-2"), "Export Filtered CSV"],
                        id="btn-export-csv", color="primary", size="sm", className="mb-2",
                    ),
                    dcc.Download(id="download-csv"),
                ],
            ),
            dash_table.DataTable(
                id="data-table",
                columns=[{"name": c.replace("_", " ").title(), "id": c} for c in columns],
                data=df[columns].head(200).to_dict("records"),
                page_size=15,
                sort_action="native",
                filter_action="native",
                fixed_rows={"headers": True},
                style_table={"overflowX": "auto", "maxHeight": "600px"},
                style_cell={"padding": "8px", "fontFamily": "Inter, sans-serif", "fontSize": "13px"},
                style_header={"fontWeight": "600"},
            ),
        ],
        className="page-content",
    )


def about_layout(df):
    return html.Div(
        [
            html.Div(
                [
                    html.H4("About This Dashboard"),
                    html.P(
                        "This dashboard analyzes cost-of-living data across 50 Bangalore "
                        "localities, 10 spending categories, and 18 service providers, "
                        "covering rent, transport, groceries, gym, food delivery, "
                        "electricity, and internet costs."
                    ),
                    html.P(
                        "Data note: this dataset is synthetic (AI-generated to simulate "
                        "realistic price patterns) and is used here to demonstrate a "
                        "complete analytics pipeline — cleaning, database design, SQL "
                        "analysis, and interactive dashboarding — at city scale."
                    ),
                    html.Hr(),
                    html.H5("Tech Stack"),
                    html.Ul([
                        html.Li("Python, Pandas, NumPy — data processing"),
                        html.Li("SQLite — structured storage"),
                        html.Li("Dash + Dash Bootstrap Components — web application"),
                        html.Li("Plotly — interactive visualizations"),
                    ]),
                    html.H5("Pages"),
                    html.Ul([
                        html.Li("Dashboard — high-level KPIs and overview charts"),
                        html.Li("Analytics — cost index, distributions, correlations, trends"),
                        html.Li("Locality Explorer — heatmap, radar, treemap by locality"),
                        html.Li("Provider Comparison — head-to-head provider pricing"),
                        html.Li("Map — geographic view colored by cost index"),
                        html.Li("Raw Data — filterable, exportable data table"),
                    ]),
                ],
                className="chart-card",
                style={"maxWidth": "800px", "margin": "0 auto"},
            )
        ],
        className="page-content",
    )
