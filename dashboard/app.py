"""
app.py
Main entry point for the Bangalore Cost of Living dashboard.
Run with:  python app.py
Then open: http://127.0.0.1:8050
"""

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

from components import sidebar, topbar
from callbacks import register_callbacks
from config import APP_TITLE

# Bootstrap Icons via CDN for all the bi-* icon classes used throughout the app
BOOTSTRAP_ICONS = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
GOOGLE_FONT = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, BOOTSTRAP_ICONS, GOOGLE_FONT],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True,
    title=APP_TITLE,
    update_title=None,
)
server = app.server  # exposed for gunicorn / production WSGI servers

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="theme-store", data="light"),
        html.Div(
            [
                sidebar(),
                html.Div(
                    [
                        topbar(),
                        html.Div(id="page-content"),
                    ],
                    className="main-area",
                ),
            ],
            className="app-shell",
        ),
    ]
)

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
