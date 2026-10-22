import sqlite3
import pandas as pd

df = pd.read_csv("zomato_clean.csv")
cuisine_df = pd.read_csv("zomato_cuisine_clean.csv")

conn = sqlite3.connect("zomato.db")
df.to_sql("restaurants", conn, if_exists="replace", index=False)
cuisine_df.to_sql("restaurant_cuisines", conn, if_exists="replace", index=False)

print(pd.read_sql("SELECT COUNT(*) AS rows_in_restaurants FROM restaurants", conn))
print(pd.read_sql("SELECT COUNT(*) AS rows_in_cuisines FROM restaurant_cuisines", conn))
conn.close()