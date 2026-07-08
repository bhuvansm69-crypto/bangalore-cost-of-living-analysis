"""
utils.py
Small shared helpers used across callbacks and layouts — kept separate so
formatting logic isn't duplicated across every callback.
"""


def format_currency(value: float) -> str:
    """Format a number as Indian Rupees with thousands separators, e.g. ₹38,724."""
    try:
        return f"₹{value:,.0f}"
    except (TypeError, ValueError):
        return "₹0"


def format_count(value: int) -> str:
    """Format an integer count with thousands separators, e.g. 100,000."""
    try:
        return f"{value:,}"
    except (TypeError, ValueError):
        return "0"


def format_index(value: float) -> str:
    """Format a 0-100 index score, e.g. '46/100'."""
    try:
        return f"{value:.0f}/100"
    except (TypeError, ValueError):
        return "—"
