import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

df = pd.read_csv("zomato.csv", encoding="latin-1")
print("Raw shape:", df.shape)

# 1. Drop unneeded columns
cols_to_drop = ['url', 'address', 'phone', 'dish_liked', 'menu_item', 'reviews_list']
df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

# 2. Remove duplicates
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

# 3. Rename columns
df = df.rename(columns={
    'approx_cost(for two people)': 'cost',
    'listed_in(type)': 'service_type',
    'listed_in(city)': 'city_zone',
    'rate': 'rating'
})

# 4. Clean rating ("4.1/5", "NEW", "-")
df['rating'] = df['rating'].astype(str).str.strip().str.replace('/5', '', regex=False)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# 5. Clean cost ("1,200")
df['cost'] = df['cost'].astype(str).str.replace(',', '', regex=False)
df['cost'] = pd.to_numeric(df['cost'], errors='coerce')

# 6. Handle missing values
df = df.dropna(subset=['rating', 'cost', 'location'])
df['cuisines'] = df['cuisines'].fillna('Unknown')

# 7. Yes/No to 1/0
df['online_order'] = df['online_order'].map({'Yes': 1, 'No': 0})
df['book_table'] = df['book_table'].map({'Yes': 1, 'No': 0})

# 8. Clean text columns
for col in ['name', 'location', 'rest_type', 'cuisines', 'city_zone', 'service_type']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
df['name'] = df['name'].str.title()

# 9. New columns
df['price_bucket'] = pd.cut(df['cost'], bins=[0, 300, 600, 1000, 100000],
                            labels=['Budget', 'Mid', 'Upper-Mid', 'Premium'])
df['rating_category'] = pd.cut(df['rating'], bins=[0, 3.0, 3.5, 4.0, 5.0],
                               labels=['Poor', 'Average', 'Good', 'Excellent'])
df['num_cuisines'] = df['cuisines'].apply(lambda x: len(x.split(',')))
df['successful'] = ((df['rating'] >= 4.0) & (df['votes'] >= df['votes'].median())).astype(int)

# 10. Cuisine-level dataframe
cuisine_df = df.assign(cuisine=df['cuisines'].str.split(',')).explode('cuisine')
cuisine_df['cuisine'] = cuisine_df['cuisine'].str.strip()

# 11. Final checks and save
print("\nFinal shape:", df.shape)
print(df.dtypes)
print("\nRemaining missing values:\n", df.isnull().sum())
print("Rating range:", df['rating'].min(), "to", df['rating'].max())
print("Cost range:", df['cost'].min(), "to", df['cost'].max())

df.to_csv("zomato_clean.csv", index=False)
cuisine_df.to_csv("zomato_cuisine_clean.csv", index=False)
print("\nSaved zomato_clean.csv and zomato_cuisine_clean.csv")