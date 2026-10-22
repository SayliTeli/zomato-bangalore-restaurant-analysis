import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

conn = sqlite3.connect("zomato.db")

with open("queries.sql", encoding="utf-8") as f:
    blocks = [b.strip() for b in f.read().split(";") if b.strip()]

for block in blocks:
    title = block.splitlines()[0]
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print(pd.read_sql(block, conn).to_string(index=False))

conn.close()