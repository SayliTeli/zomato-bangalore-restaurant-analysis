import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 40)

# Change to "data/zomato.csv" if you moved the file into a data folder
df = pd.read_csv("zomato.csv", encoding="latin-1")

def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

# 1. Shape and columns
section("1. SHAPE")
print(df.shape)

section("2. COLUMN NAMES")
print(df.columns.tolist())

section("3. FIRST 5 ROWS")
print(df.head())

section("4. RANDOM 5 ROWS")
print(df.sample(5, random_state=1))

# 2. Data types
section("5. INFO (data types and non-null counts)")
df.info()

# 3. Missing values
section("6. MISSING VALUES")
missing = pd.DataFrame({
    'missing': df.isnull().sum(),
    'percent': (df.isnull().mean() * 100).round(2)
})
print(missing[missing.missing > 0].sort_values('percent', ascending=False))

# 4. Duplicates
section("7. DUPLICATES")
print("Duplicate rows:", df.duplicated().sum())

# 5. Messy columns
section("8. RATE COLUMN (unique values)")
print(df['rate'].value_counts().head(15))

section("9. COST COLUMN (sample values)")
print(df['approx_cost(for two people)'].unique()[:20])

section("10. CATEGORICAL COLUMNS")
print(df['online_order'].value_counts())
print(df['book_table'].value_counts())
print("Unique locations:", df['location'].nunique())
print(df['rest_type'].value_counts().head(10))
print(df['cuisines'].value_counts().head(10))

section("11. TOP RESTAURANT NAMES (chains)")
print(df['name'].value_counts().head(10))

# 6. Numeric summary
section("12. NUMERIC SUMMARY")
print(df.describe())

section("13. TEXT SUMMARY")
print(df.describe(include='object'))

# 7. Missing values chart (saved as image)
plt.figure(figsize=(10, 4))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False)
plt.title("Missing values map")
plt.tight_layout()
plt.savefig("missing_values.png")
print("\nSaved missing_values.png in your project folder")