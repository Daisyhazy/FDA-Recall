import pandas as pd

df = pd.read_csv("device_recalls_raw.csv")

print("Shape (rows, columns):", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))
