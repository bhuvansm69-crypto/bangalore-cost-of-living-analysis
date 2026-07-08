"""
config.py
Central configuration: file paths, color palettes, and static reference data
(locality coordinates) used across the dashboard.
"""

import os

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "bangalore_cost_tracker_clean.csv")
DB_PATH = os.path.join(BASE_DIR, "data","processed", "bangalore_cost_tracker.db")

# ------------------------------------------------------------------
# App metadata
# ------------------------------------------------------------------
APP_TITLE = "Bangalore Cost of Living Analysis"
APP_SUBTITLE = "A Locality-Wise Comparative Study"

# ------------------------------------------------------------------
# Category display config
# ------------------------------------------------------------------
CATEGORY_LABELS = {
    "rent": "Rent",
    "auto_fare": "Auto Fare",
    "metro": "Metro",
    "bmtc": "BMTC Bus",
    "fuel": "Fuel",
    "grocery": "Grocery",
    "gym": "Gym",
    "delivery_app": "Food Delivery",
    "electricity": "Electricity",
    "internet": "Internet",
}

# Categories where a LOWER price is better (used for affordability scoring).
# All current categories are cost categories, so all are "lower is better".
COST_CATEGORIES = list(CATEGORY_LABELS.keys())

# ------------------------------------------------------------------
# Approximate locality coordinates (Bangalore, India)
# NOTE: These are approximate central-area coordinates for each named
# locality, intended for relative map visualization only — not
# survey-grade GPS accuracy.
# ------------------------------------------------------------------
LOCALITY_COORDS = {
    "Anekal": (12.7106, 77.6960),
    "Arekere": (12.8880, 77.5980),
    "Attibele": (12.7770, 77.7710),
    "BTM Layout": (12.9166, 77.6101),
    "Banashankari": (12.9250, 77.5460),
    "Banaswadi": (13.0140, 77.6510),
    "Basavanagudi": (12.9420, 77.5730),
    "Bellandur": (12.9260, 77.6770),
    "Bommanahalli": (12.9080, 77.6220),
    "Brookefield": (12.9650, 77.7180),
    "CV Raman Nagar": (12.9830, 77.6650),
    "Chandapura": (12.8090, 77.7060),
    "Cooke Town": (12.9930, 77.6210),
    "Domlur": (12.9610, 77.6390),
    "Electronic City": (12.8450, 77.6600),
    "Frazer Town": (12.9970, 77.6120),
    "HSR Layout": (12.9120, 77.6440),
    "Hebbal": (13.0350, 77.5970),
    "Hennur": (13.0390, 77.6300),
    "Hoodi": (12.9910, 77.7130),
    "Indiranagar": (12.9780, 77.6410),
    "JP Nagar": (12.9080, 77.5850),
    "Jayanagar": (12.9300, 77.5830),
    "KR Puram": (12.9930, 77.6950),
    "Kadubeesanahalli": (12.9370, 77.6980),
    "Kalyan Nagar": (13.0220, 77.6390),
    "Kengeri": (12.9080, 77.4830),
    "Kodihalli": (12.9600, 77.6480),
    "Koramangala": (12.9350, 77.6140),
    "Mahadevapura": (12.9900, 77.6960),
    "Malleshwaram": (13.0030, 77.5700),
    "Mallespalya": (12.9280, 77.6270),
    "Marathahalli": (12.9560, 77.7010),
    "Nagawara": (13.0440, 77.6220),
    "Peenya": (13.0290, 77.5200),
    "RR Nagar": (12.9230, 77.5210),
    "Rajajinagar": (12.9910, 77.5530),
    "Richmond Town": (12.9630, 77.6070),
    "Sahakar Nagar": (13.0630, 77.5940),
    "Sanjay Nagar": (13.0210, 77.5810),
    "Sarjapur": (12.8990, 77.6870),
    "Shivajinagar": (12.9860, 77.6050),
    "Silk Board": (12.9170, 77.6230),
    "Ulsoor": (12.9810, 77.6220),
    "Varthur": (12.9420, 77.7400),
    "Vidyaranyapura": (13.0680, 77.5560),
    "Whitefield": (12.9700, 77.7500),
    "Wilson Garden": (12.9520, 77.5960),
    "Yelahanka": (13.1010, 77.5960),
    "Yeshwanthpur": (13.0280, 77.5540),
}

# ------------------------------------------------------------------
# Theme colors
# ------------------------------------------------------------------
THEME = {
    "light": {
        "bg": "#f4f6fb",
        "surface": "rgba(255,255,255,0.65)",
        "surface_solid": "#ffffff",
        "text": "#1c2333",
        "text_muted": "#6b7280",
        "border": "rgba(15,23,42,0.08)",
        "accent": "#6366f1",
        "accent2": "#22c55e",
        "shadow": "0 8px 32px rgba(31, 38, 135, 0.08)",
        "sidebar_bg": "linear-gradient(180deg, #ffffff 0%, #f0f1fb 100%)",
        "chart_template": "plotly_white",
    },
    "dark": {
        "bg": "#0f1220",
        "surface": "rgba(255,255,255,0.06)",
        "surface_solid": "#171a2b",
        "text": "#e8eaf6",
        "text_muted": "#9ca3af",
        "border": "rgba(255,255,255,0.08)",
        "accent": "#818cf8",
        "accent2": "#4ade80",
        "shadow": "0 8px 32px rgba(0,0,0,0.4)",
        "sidebar_bg": "linear-gradient(180deg, #171a2b 0%, #0f1220 100%)",
        "chart_template": "plotly_dark",
    },
}

CHART_COLOR_SEQUENCE = [
    "#6366f1", "#22c55e", "#f59e0b", "#ef4444", "#06b6d4",
    "#a855f7", "#ec4899", "#84cc16", "#3b82f6", "#f97316",
]
