"""
=============================================================
Bangalore Cost of Living Analysis
Phase 2 - SQLite Database Creation

Author: Bhuvan S M
=============================================================
"""

from pathlib import Path
import sqlite3
import pandas as pd


# =============================================================
# PROJECT PATHS
# =============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "bangalore_cost_tracker_clean.csv"
)

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "bangalore_cost_tracker.db"
)


# =============================================================
# LOAD DATA
# =============================================================

print("=" * 70)
print("Loading cleaned dataset...")

df = pd.read_csv(CSV_PATH)

print(f"Rows Loaded : {len(df):,}")


# =============================================================
# CREATE DATABASE
# =============================================================

print("\nCreating SQLite database...")

connection = sqlite3.connect(DATABASE_PATH)

df.to_sql(
    name="cost_of_living",
    con=connection,
    if_exists="replace",
    index=False
)

cursor = connection.cursor()


# =============================================================
# VERIFY DATABASE
# =============================================================

cursor.execute("SELECT COUNT(*) FROM cost_of_living")
total_rows = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(DISTINCT Locality)
FROM cost_of_living
""")
localities = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(DISTINCT Category)
FROM cost_of_living
""")
categories = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(DISTINCT Provider)
FROM cost_of_living
""")
providers = cursor.fetchone()[0]


connection.commit()
connection.close()


# =============================================================
# SUMMARY
# =============================================================

print("\nDatabase Created Successfully!")

print("-" * 50)
print(f"Total Records : {total_rows:,}")
print(f"Localities    : {localities}")
print(f"Categories    : {categories}")
print(f"Providers     : {providers}")
print("-" * 50)

print("\nDatabase Location:")
print(DATABASE_PATH)

print("\nSQLite database is ready.")
print("=" * 70)