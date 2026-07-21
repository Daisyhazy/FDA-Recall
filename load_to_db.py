import pandas as pd
import sqlite3

df = pd.read_csv("device_recalls_raw.csv")

conn = sqlite3.connect("recalls.db")
df.to_sql("recalls", conn, if_exists="replace", index=False)

print("Loaded into recalls.db")
print("Row count:", conn.execute("SELECT COUNT(*) FROM recalls").fetchone()[0])

conn.close()

