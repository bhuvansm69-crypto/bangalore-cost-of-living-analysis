import pandas as pd
import numpy as np

print("="*70)
print("BANGALORE COST OF LIVING - STATISTICAL ANALYSIS")
print("="*70)

# Load Dataset
df = pd.read_csv("data/processed/bangalore_cost_tracker_clean.csv")

price = df["Price_INR"]

print("\nDATASET STATISTICS")
print("-"*70)

print(f"Total Records           : {len(df):,}")
print(f"Mean Price              : ₹{price.mean():.2f}")
print(f"Median Price            : ₹{price.median():.2f}")
print(f"Mode Price              : ₹{price.mode().iloc[0]:.2f}")
print(f"Minimum Price           : ₹{price.min():.2f}")
print(f"Maximum Price           : ₹{price.max():.2f}")

print("\nDISPERSION")
print("-"*70)

print(f"Variance                : {price.var():.2f}")
print(f"Standard Deviation      : {price.std():.2f}")
print(f"Range                   : {price.max()-price.min():.2f}")

print("\nPERCENTILES")
print("-"*70)

print(f"25th Percentile         : ₹{price.quantile(.25):.2f}")
print(f"50th Percentile         : ₹{price.quantile(.50):.2f}")
print(f"75th Percentile         : ₹{price.quantile(.75):.2f}")
print(f"90th Percentile         : ₹{price.quantile(.90):.2f}")

print("\nINTERQUARTILE RANGE")
print("-"*70)

Q1 = price.quantile(.25)
Q3 = price.quantile(.75)

IQR = Q3-Q1

print(f"IQR                     : {IQR:.2f}")

lower = Q1-1.5*IQR
upper = Q3+1.5*IQR

print(f"Lower Bound             : {lower:.2f}")
print(f"Upper Bound             : {upper:.2f}")

outliers = df[(price<lower)|(price>upper)]

print(f"\nTotal Outliers          : {len(outliers)}")

print("\nCATEGORY STATISTICS")
print("-"*70)

summary = df.groupby("Category")["Price_INR"].agg(
    ["count","mean","median","min","max","std"]
)

print(summary.round(2))

print("\nLOCALITY STATISTICS")
print("-"*70)

locality = df.groupby("Locality")["Price_INR"].mean()

print(locality.sort_values(ascending=False).head(10))

print("\nCompleted Successfully")