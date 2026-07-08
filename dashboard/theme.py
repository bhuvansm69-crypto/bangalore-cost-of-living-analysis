"""
theme.py
Helpers for applying light/dark theme styling consistently to every Plotly
chart, so a single toggle switches the whole dashboard's look.
"""

from config import THEME, CHART_COLOR_SEQUENCE


def get_theme(mode: str = "light") -> dict:
    """Return the theme dict for 'light' or 'dark' (defaults to light on bad input)."""
    return THEME.get(mode, THEME["light"])


def style_figure(fig, mode: str = "light"):
    """Apply consistent template, colors, fonts, and transparent backgrounds to a figure."""
    t = get_theme(mode)
    fig.update_layout(
        template=t["chart_template"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, sans-serif", color=t["text"], size=13),
        colorway=CHART_COLOR_SEQUENCE,
        title_text=None,
        autosize=True,
        margin=dict(t=20, l=36, r=16, b=36),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(
            bgcolor=t["surface_solid"],
            font_color=t["text"],
            font_size=12,
        ),
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig
