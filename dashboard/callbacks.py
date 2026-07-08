"""
callbacks.py
All Dash callbacks: page routing, theme toggle, sidebar collapse, filter-driven
chart updates for every page, data table filtering, and CSV export.

Design note: filter components (filter-locality, filter-category, etc.) share
the same IDs across every page layout in layouts.py. Only one page's layout is
mounted in the DOM at a time (swapped by the routing callback), so this is
safe — each page-specific callback below only fires when its own page (and
therefore its own filter/chart component instances) is actually on screen.
"""

from dash import Input, Output, State, dcc, html, ctx, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import layouts
import charts
from components import sidebar, topbar, insight_card, NAV_ITEMS
from data import load_data, filter_data, compute_kpis, generate_insights, top_recommendations
from utils import format_currency, format_count, format_index

DF = load_data()


def _apply_filters(locality, category, provider, search, start_date, end_date, price_range):
    return filter_data(
        DF,
        localities=locality, categories=category, providers=provider,
        date_range=(start_date, end_date), price_range=price_range, search=search,
    )


def register_callbacks(app):

    # ------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
    )
    def route(pathname):
        pages = {
            "/": layouts.dashboard_layout,
            "/analytics": layouts.analytics_layout,
            "/locality": layouts.locality_layout,
            "/providers": layouts.providers_layout,
            "/map": layouts.map_layout,
            "/data": layouts.data_layout,
            "/about": layouts.about_layout,
        }
        page_fn = pages.get(pathname, layouts.dashboard_layout)
        return page_fn(DF)

    @app.callback(
        [Output(f"nav-{href.strip('/') or 'home'}", "className") for _, href, _ in NAV_ITEMS],
        Input("url", "pathname"),
    )
    def highlight_active_nav(pathname):
        return [
            "nav-item active" if pathname == href else "nav-item"
            for _, href, _ in NAV_ITEMS
        ]

    # ------------------------------------------------------------
    # Theme + sidebar collapse (clientside, instant, no server round-trip)
    # ------------------------------------------------------------
    app.clientside_callback(
        """
        function(isDark) {
            document.body.setAttribute('data-theme', isDark ? 'dark' : 'light');
            return isDark ? 'bi bi-sun' : 'bi bi-moon-stars';
        }
        """,
        Output("theme-icon", "className"),
        Input("theme-switch", "value"),
    )

    # Track the current theme as a store, mirrored from the switch, so chart
    # callbacks (which run server-side and can't read document.body) know
    # which Plotly template to apply.
    @app.callback(Output("theme-store", "data"), Input("theme-switch", "value"))
    def sync_theme_store(is_dark):
        return "dark" if is_dark else "light"

    # ------------------------------------------------------------
    # Reset filters (shared across pages — see module docstring)
    # ------------------------------------------------------------
    @app.callback(
        [
            Output("filter-locality", "value"),
            Output("filter-category", "value"),
            Output("filter-provider", "value"),
            Output("filter-search", "value"),
            Output("filter-date-range", "start_date"),
            Output("filter-date-range", "end_date"),
            Output("filter-price-range", "value"),
        ],
        Input("btn-reset-filters", "n_clicks"),
        prevent_initial_call=True,
    )
    def reset_filters(n_clicks):
        min_date, max_date = DF["timestamp"].min().date(), DF["timestamp"].max().date()
        min_price, max_price = float(DF["price"].min()), float(DF["price"].max())
        return None, None, None, "", min_date, max_date, [min_price, max_price]

    # ------------------------------------------------------------
    # Dashboard page
    # ------------------------------------------------------------
    @app.callback(
        [
            Output("kpi-total-records", "children"),
            Output("kpi-total-localities", "children"),
            Output("kpi-total-categories", "children"),
            Output("kpi-total-providers", "children"),
            Output("kpi-avg-cost", "children"),
            Output("kpi-avg-rent", "children"),
            Output("kpi-avg-grocery", "children"),
            Output("kpi-avg-delivery", "children"),
            Output("kpi-max-cost", "children"),
            Output("kpi-min-cost", "children"),
            Output("kpi-cost-index", "children"),
            Output("chart-top-expensive", "figure"),
            Output("chart-top-affordable", "figure"),
            Output("chart-category-avg", "figure"),
            Output("chart-monthly-trend", "figure"),
            Output("chart-sunburst", "figure"),
        ],
        [
            Input("filter-locality", "value"),
            Input("filter-category", "value"),
            Input("filter-provider", "value"),
            Input("filter-search", "value"),
            Input("filter-date-range", "start_date"),
            Input("filter-date-range", "end_date"),
            Input("filter-price-range", "value"),
            Input("theme-store", "data"),
        ],
    )
    def update_dashboard(locality, category, provider, search, start_date, end_date, price_range, theme):
        theme = theme or "light"
        sub = _apply_filters(locality, category, provider, search, start_date, end_date, price_range)
        k = compute_kpis(sub)
        return (
            format_count(k['total_records']),
            f"{k['total_localities']}",
            f"{k['total_categories']}",
            f"{k['total_providers']}",
            format_currency(k['avg_cost']),
            format_currency(k['avg_rent']),
            format_currency(k['avg_grocery']),
            format_currency(k['avg_delivery']),
            format_currency(k['max_cost']),
            format_currency(k['min_cost']),
            format_index(k['cost_index']),
            charts.top_expensive_localities(sub, theme),
            charts.top_affordable_localities(sub, theme),
            charts.category_average_bar(sub, theme),
            charts.monthly_trend_line(sub, theme),
            charts.sunburst_locality_category_provider(sub, theme),
        )

    # ------------------------------------------------------------
    # Analytics page
    # ------------------------------------------------------------
    @app.callback(
        [
            Output("insights-container", "children"),
            Output("chart-cost-index", "figure"),
            Output("chart-top5-bottom5", "figure"),
            Output("chart-histogram", "figure"),
            Output("chart-box", "figure"),
            Output("chart-violin", "figure"),
            Output("chart-correlation", "figure"),
            Output("chart-daytype", "figure"),
            Output("chart-yearly", "figure"),
            Output("chart-area", "figure"),
        ],
        [
            Input("filter-locality", "value"),
            Input("filter-category", "value"),
            Input("filter-provider", "value"),
            Input("filter-search", "value"),
            Input("filter-date-range", "start_date"),
            Input("filter-date-range", "end_date"),
            Input("filter-price-range", "value"),
            Input("theme-store", "data"),
        ],
    )
    def update_analytics(locality, category, provider, search, start_date, end_date, price_range, theme):
        theme = theme or "light"
        sub = _apply_filters(locality, category, provider, search, start_date, end_date, price_range)

        insights = generate_insights(sub)
        recs = top_recommendations(sub)
        insight_children = [insight_card("bi-lightbulb", txt) for txt in insights]
        if recs:
            insight_children.append(
                insight_card("bi-star", "Most affordable picks: " + "; ".join(recs))
            )

        return (
            insight_children,
            charts.cost_index_ranking(sub, theme),
            charts.top5_vs_bottom5(sub, theme),
            charts.price_histogram(sub, theme),
            charts.price_box(sub, theme),
            charts.price_violin(sub, theme),
            charts.correlation_matrix(sub, theme),
            charts.stacked_bar_daytype(sub, theme),
            charts.yearly_trend_bar(sub, theme),
            charts.area_trend(sub, theme),
        )

    # ------------------------------------------------------------
    # Locality Explorer page
    # ------------------------------------------------------------
    @app.callback(
        [
            Output("chart-heatmap", "figure"),
            Output("chart-radar", "figure"),
            Output("chart-treemap", "figure"),
            Output("chart-scatter-demand", "figure"),
        ],
        [
            Input("filter-locality", "value"),
            Input("filter-category", "value"),
            Input("filter-provider", "value"),
            Input("filter-search", "value"),
            Input("filter-date-range", "start_date"),
            Input("filter-date-range", "end_date"),
            Input("filter-price-range", "value"),
            Input("theme-store", "data"),
        ],
    )
    def update_locality(locality, category, provider, search, start_date, end_date, price_range, theme):
        theme = theme or "light"
        sub = _apply_filters(locality, category, provider, search, start_date, end_date, price_range)
        return (
            charts.heatmap_locality_category(sub, theme),
            charts.radar_top_localities(sub, theme),
            charts.treemap_category_locality(sub, theme),
            charts.scatter_price_by_demand(sub, theme),
        )

    # ------------------------------------------------------------
    # Provider Comparison page
    # ------------------------------------------------------------
    @app.callback(
        [
            Output("chart-provider-bar", "figure"),
            Output("chart-bubble", "figure"),
            Output("chart-swiggy-zomato", "figure"),
            Output("chart-ola-uber", "figure"),
        ],
        [
            Input("filter-locality", "value"),
            Input("filter-category", "value"),
            Input("filter-provider", "value"),
            Input("filter-search", "value"),
            Input("filter-date-range", "start_date"),
            Input("filter-date-range", "end_date"),
            Input("filter-price-range", "value"),
            Input("provider-category-select", "value"),
            Input("theme-store", "data"),
        ],
    )
    def update_providers(locality, category, provider, search, start_date, end_date, price_range, selected_cat, theme):
        theme = theme or "light"
        sub = _apply_filters(locality, category, provider, search, start_date, end_date, price_range)
        return (
            charts.provider_comparison_bar(sub, theme, selected_cat),
            charts.bubble_category_provider(sub, theme),
            charts.head_to_head(sub, theme, "Swiggy", "Zomato", "delivery_app"),
            charts.head_to_head(sub, theme, "Ola", "Uber", "auto_fare"),
        )

    # ------------------------------------------------------------
    # Map page
    # ------------------------------------------------------------
    @app.callback(
        Output("chart-map", "figure"),
        [
            Input("filter-locality", "value"),
            Input("filter-category", "value"),
            Input("filter-provider", "value"),
            Input("filter-search", "value"),
            Input("filter-date-range", "start_date"),
            Input("filter-date-range", "end_date"),
            Input("filter-price-range", "value"),
            Input("theme-store", "data"),
        ],
    )
    def update_map(locality, category, provider, search, start_date, end_date, price_range, theme):
        theme = theme or "light"
        sub = _apply_filters(locality, category, provider, search, start_date, end_date, price_range)
        return charts.locality_map(sub, theme)

    # ------------------------------------------------------------
    # Raw Data page: table + CSV export
    # ------------------------------------------------------------
    @app.callback(
        Output("data-table", "data"),
        [
            Input("filter-locality", "value"),
            Input("filter-category", "value"),
            Input("filter-provider", "value"),
            Input("filter-search", "value"),
            Input("filter-date-range", "start_date"),
            Input("filter-date-range", "end_date"),
            Input("filter-price-range", "value"),
        ],
    )
    def update_table(locality, category, provider, search, start_date, end_date, price_range):
        sub = _apply_filters(locality, category, provider, search, start_date, end_date, price_range)
        columns = ["timestamp", "locality", "category", "item", "provider", "price", "day_type", "weather", "demand"]
        return sub[columns].head(2000).to_dict("records")

    @app.callback(
        Output("download-csv", "data"),
        Input("btn-export-csv", "n_clicks"),
        [
            State("filter-locality", "value"),
            State("filter-category", "value"),
            State("filter-provider", "value"),
            State("filter-search", "value"),
            State("filter-date-range", "start_date"),
            State("filter-date-range", "end_date"),
            State("filter-price-range", "value"),
        ],
        prevent_initial_call=True,
    )
    def export_csv(n_clicks, locality, category, provider, search, start_date, end_date, price_range):
        sub = _apply_filters(locality, category, provider, search, start_date, end_date, price_range)
        return dcc.send_data_frame(sub.to_csv, "bangalore_cost_data_filtered.csv", index=False)

    # Expose callback functions directly on the app object so they can be
    # unit-tested without going through Dash's HTTP layer (useful in CI or
    # a quick local sanity check — see tests/test_callbacks.py).
    app._testable_callbacks = {
        "route": route,
        "update_dashboard": update_dashboard,
        "update_analytics": update_analytics,
        "update_locality": update_locality,
        "update_providers": update_providers,
        "update_map": update_map,
        "update_table": update_table,
        "reset_filters": reset_filters,
    }
