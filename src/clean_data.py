"""
Bangalore Cost of Living Analysis
---------------------------------
Data Cleaning Script

Author: Bhuvan S M
"""

from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "bangalore_cost_tracker_synthetic_100000.xlsx"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_CSV = PROCESSED_DIR / "bangalore_cost_tracker_clean.csv"


# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 70)
print("Loading dataset...")

df = pd.read_excel(RAW_DATA_PATH)

print("Dataset loaded successfully.")
print("=" * 70)


# ============================================================
# DATASET INFORMATION
# ============================================================

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================================
# DATA CLEANING
# ============================================================

print("\nCleaning dataset...")

# Remove duplicate rows
df = df.drop_duplicates()

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Remove whitespace
text_columns = [
    "Locality",
    "Category",
    "Item_or_Route",
    "Provider",
    "DayType",
    "Weather",
    "Demand",
    "Notes",
]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# Remove invalid prices
df = df[df["Price_INR"] > 0]

# Sort dataset
df = df.sort_values("Timestamp")

# Reset index
df.reset_index(drop=True, inplace=True)

print("Cleaning completed.")


# ============================================================
# SUMMARY
# ============================================================

print("\nFinal Shape:")
print(df.shape)

print("\nUnique Localities:")
print(df["Locality"].nunique())

print("\nUnique Categories:")
print(df["Category"].nunique())

print("\nProviders:")
print(df["Provider"].nunique())


# ============================================================
# EXPORT CLEAN DATA
# ============================================================

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_CSV, index=False)

print("\nClean dataset saved successfully!")

print(f"\nLocation:\n{OUTPUT_CSV}")

print("\nData Cleaning Completed Successfully!")
print("=" * 70)