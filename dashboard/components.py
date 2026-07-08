"""
components.py
Reusable UI building blocks: KPI cards, sidebar navigation items, and the
shared filter panel. Kept separate from layouts.py so the same pieces can be
composed across multiple pages without duplication.
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

from dashboard.config import CATEGORY_LABELS


# ------------------------------------------------------------------
# KPI Card
# ------------------------------------------------------------------

def kpi_card(title: str, value: str, icon: str, card_id: str, accent: str = "primary"):
    """A single glassmorphism-style KPI card with an icon, title, and value."""
    return dbc.Col(
        html.Div(
            [
                html.Div(html.I(className=f"bi {icon}"), className=f"kpi-icon kpi-icon-{accent}"),
                html.Div(
                    [
                        html.Div(title, className="kpi-title"),
                        html.Div(value, className="kpi-value", id=card_id),
                    ]
                ),
            ],
            className="kpi-card",
        ),
        xs=12, sm=6, md=4, lg=3,
        className="mb-3",
    )


def kpi_row():
    """The full row of top KPI cards. Values are filled in by a callback."""
    cards = [
        ("Total Records", "kpi-total-records", "bi-database", "primary"),
        ("Localities", "kpi-total-localities", "bi-geo-alt", "success"),
        ("Categories", "kpi-total-categories", "bi-tags", "warning"),
        ("Providers", "kpi-total-providers", "bi-building", "info"),
        ("Avg Cost", "kpi-avg-cost", "bi-currency-rupee", "primary"),
        ("Avg Rent", "kpi-avg-rent", "bi-house-door", "danger"),
        ("Avg Grocery", "kpi-avg-grocery", "bi-cart", "success"),
        ("Avg Delivery", "kpi-avg-delivery", "bi-bicycle", "warning"),
        ("Max Cost", "kpi-max-cost", "bi-arrow-up-circle", "danger"),
        ("Min Cost", "kpi-min-cost", "bi-arrow-down-circle", "success"),
        ("Cost of Living Index", "kpi-cost-index", "bi-graph-up-arrow", "info"),
    ]
    return dbc.Row(
        [kpi_card(title, "—", icon, cid, accent) for title, cid, icon, accent in cards],
        className="g-3",
    )


# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------

NAV_ITEMS = [
    ("Dashboard", "/", "bi-speedometer2"),
    ("Analytics", "/analytics", "bi-bar-chart-line"),
    ("Locality Explorer", "/locality", "bi-geo"),
    ("Provider Comparison", "/providers", "bi-shop"),
    ("Map", "/map", "bi-map"),
    ("Raw Data", "/data", "bi-table"),
    ("About", "/about", "bi-info-circle"),
]


def sidebar():
    return html.Div(
        [
            html.Div(
                [
                    html.I(className="bi bi-bar-chart-steps sidebar-logo-icon"),
                    html.Span("Cost Tracker", className="sidebar-logo-text"),
                ],
                className="sidebar-logo",
            ),
            html.Div(
                [
                    dcc.Link(
                        [html.I(className=f"bi {icon} nav-icon"), html.Span(label, className="nav-label")],
                        href=href,
                        className="nav-item",
                        id=f"nav-{href.strip('/') or 'home'}",
                    )
                    for label, href, icon in NAV_ITEMS
                ],
                className="sidebar-nav",
            ),
            html.Div(
                [
                    html.I(className="bi bi-moon-stars", id="theme-icon"),
                    dbc.Switch(id="theme-switch", value=False, className="theme-switch"),
                ],
                className="sidebar-footer",
            ),
        ],
        className="sidebar",
        id="sidebar",
    )


def topbar():
    return html.Div(
        [
            html.Button(html.I(className="bi bi-list"), id="sidebar-toggle", className="icon-btn"),
            html.Div(
                [
                    html.H5("Bangalore Cost of Living Analysis", className="topbar-title"),
                    html.Div("A Locality-Wise Comparative Study", className="topbar-subtitle"),
                ],
                className="topbar-titles",
            ),
        ],
        className="topbar",
    )


# ------------------------------------------------------------------
# Filter panel (shared across pages)
# ------------------------------------------------------------------

def filter_panel(df):
    localities = sorted(df["locality"].unique())
    categories = sorted(df["category"].unique())
    providers = sorted(df["provider"].unique())
    min_price, max_price = float(df["price"].min()), float(df["price"].max())
    min_date, max_date = df["timestamp"].min().date(), df["timestamp"].max().date()

    return html.Div(
        [
            html.Div("Filters", className="filter-panel-title"),
            dbc.Row(
                [
                    dbc.Col([
                        html.Label("Locality", className="filter-label"),
                        dcc.Dropdown(
                            id="filter-locality",
                            options=[{"label": l, "value": l} for l in localities],
                            multi=True, placeholder="All localities",
                        ),
                    ], md=3, className="mb-2"),

                    dbc.Col([
                        html.Label("Category", className="filter-label"),
                        dcc.Dropdown(
                            id="filter-category",
                            options=[{"label": CATEGORY_LABELS.get(c, c.title()), "value": c} for c in categories],
                            multi=True, placeholder="All categories",
                        ),
                    ], md=3, className="mb-2"),

                    dbc.Col([
                        html.Label("Provider", className="filter-label"),
                        dcc.Dropdown(
                            id="filter-provider",
                            options=[{"label": p, "value": p} for p in providers],
                            multi=True, placeholder="All providers",
                        ),
                    ], md=3, className="mb-2"),

                    dbc.Col([
                        html.Label("Search", className="filter-label"),
                        dbc.Input(id="filter-search", placeholder="Search locality, item, provider...", type="text"),
                    ], md=3, className="mb-2"),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([
                        html.Label("Date Range", className="filter-label"),
                        dcc.DatePickerRange(
                            id="filter-date-range",
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            start_date=min_date,
                            end_date=max_date,
                            display_format="YYYY-MM-DD",
                        ),
                    ], md=5, className="mb-2"),

                    dbc.Col([
                        html.Label("Price Range (₹)", className="filter-label"),
                        dcc.RangeSlider(
                            id="filter-price-range",
                            min=min_price, max=max_price,
                            value=[min_price, max_price],
                            tooltip={"placement": "bottom", "always_visible": False},
                            allowCross=False,
                        ),
                    ], md=5, className="mb-2"),

                    dbc.Col([
                        html.Label("\u00a0", className="filter-label d-block"),
                        dbc.ButtonGroup([
                            dbc.Button("Apply", id="btn-apply-filters", color="primary", size="sm"),
                            dbc.Button("Reset", id="btn-reset-filters", color="secondary", size="sm", outline=True),
                        ], className="w-100"),
                    ], md=2, className="mb-2"),
                ]
            ),
        ],
        className="filter-panel",
    )


def chart_card(title: str, chart_id: str, md=6, extra=None):
    """A card wrapping a single dcc.Graph, with a title header."""
    children = [html.Div(title, className="chart-card-title")]
    if extra:
        children.append(extra)
    children.append(
        dcc.Graph(
            id=chart_id,
            config={"displaylogo": False, "responsive": True},
            className="chart-graph",
            style={"width": "100%", "height": "420px"},
        )
    )
    return dbc.Col(html.Div(children, className="chart-card"), xs=12, lg=md, className="mb-4")


def insight_card(icon: str, text: str):
    return html.Div(
        [html.I(className=f"bi {icon} insight-icon"), html.Span(text)],
        className="insight-card",
    )
