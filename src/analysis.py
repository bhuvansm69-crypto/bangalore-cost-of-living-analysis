import pandas as pd

print("="*60)
print("BANGALORE COST OF LIVING ANALYSIS")
print("="*60)

df = pd.read_csv("data/processed/bangalore_cost_tracker_clean.csv")

print("\nDataset Loaded Successfully")

print("\nShape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nFirst Five Rows")
print(df.head())

print("\nDataset Information")
print(df.info())

print("\nSummary Statistics")
print(df.describe(include='all'))

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Records")
print(df.duplicated().sum())

print("\nUnique Localities")
print(df["Locality"].nunique())

print("\nUnique Categories")
print(df["Category"].nunique())

print("\nUnique Providers")
print(df["Provider"].nunique())

print("\nAverage Price")
print(df["Price_INR"].mean())

print("\nMaximum Price")
print(df["Price_INR"].max())

print("\nMinimum Price")
print(df["Price_INR"].min())

print("\nCompleted Successfully")