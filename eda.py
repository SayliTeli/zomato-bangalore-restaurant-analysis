import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
sns.set_style("whitegrid")
os.makedirs("charts", exist_ok=True)

df = pd.read_csv("zomato_clean.csv")
cuisine_df = pd.read_csv("zomato_cuisine_clean.csv")

price_order = ['Budget', 'Mid', 'Upper-Mid', 'Premium']
df['price_bucket'] = pd.Categorical(df['price_bucket'], categories=price_order, ordered=True)

def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def save(name):
    plt.tight_layout()
    plt.savefig(f"charts/{name}.png", dpi=150)
    plt.close()
    print(f"Saved charts/{name}.png")

# ---------- Q1: Does higher price mean higher rating? ----------
section("Q1. RATING vs PRICE")
print("Correlation (cost vs rating):", round(df['cost'].corr(df['rating']), 3))

by_price = df.groupby('price_bucket', observed=True).agg(
    restaurants=('name', 'count'),
    avg_rating=('rating', 'mean'),
    median_rating=('rating', 'median'),
    avg_votes=('votes', 'mean')
).round(2)
print(by_price)

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='cost', y='rating', alpha=0.2)
plt.title("Cost for two vs rating")
save("q1_cost_vs_rating_scatter")

plt.figure(figsize=(7, 4))
sns.barplot(data=df, x='price_bucket', y='rating', order=price_order, errorbar=None)
plt.ylim(3, 4.5)
plt.title("Average rating by price bucket")
save("q1_rating_by_price_bucket")

# ---------- Q2: Cuisine popularity ----------
section("Q2. CUISINES")
top_count = cuisine_df['cuisine'].value_counts().head(10)
top_votes = cuisine_df.groupby('cuisine')['votes'].sum().nlargest(10)
cuisine_stats = cuisine_df.groupby('cuisine').agg(
    restaurants=('name', 'count'), avg_rating=('rating', 'mean')
)
top_rated = cuisine_stats[cuisine_stats.restaurants >= 50].nlargest(10, 'avg_rating').round(2)

print("Most common cuisines:\n", top_count)
print("\nMost in demand (total votes):\n", top_votes)
print("\nBest rated (min 50 restaurants):\n", top_rated)

plt.figure(figsize=(8, 5))
sns.barplot(x=top_count.values, y=top_count.index, color="#e23744")
plt.title("Top 10 cuisines by number of restaurants")
save("q2_top_cuisines_count")

plt.figure(figsize=(8, 5))
sns.barplot(x=top_rated['avg_rating'], y=top_rated.index, color="#2a9d8f")
plt.xlim(3.5, 4.5)
plt.title("Best rated cuisines (min 50 restaurants)")
save("q2_top_cuisines_rating")

# ---------- Q3: Location trends and market gaps ----------
section("Q3. LOCATIONS")
loc = df.groupby('location').agg(
    restaurants=('name', 'count'),
    avg_cost=('cost', 'mean'),
    avg_rating=('rating', 'mean'),
    total_votes=('votes', 'sum')
).round(2)

print("Most crowded areas:\n", loc.nlargest(10, 'restaurants'))

# Market gap: high rating, few restaurants (at least 20 so the average is reliable)
gap = loc[(loc.restaurants >= 20) & (loc.restaurants <= loc.restaurants.median())] \
        .nlargest(10, 'avg_rating')
print("\nPossible market gaps (high rating, low competition):\n", gap)

plt.figure(figsize=(8, 5))
sns.barplot(x=loc.nlargest(10, 'restaurants')['restaurants'],
            y=loc.nlargest(10, 'restaurants').index, color="#264653")
plt.title("Top 10 areas by number of restaurants")
save("q3_top_locations")

# ---------- Q4: Online order and table booking ----------
section("Q4. ONLINE ORDER & TABLE BOOKING")
print(df.groupby('online_order')[['rating', 'cost', 'votes']].mean().round(2))
print(df.groupby('book_table')[['rating', 'cost', 'votes']].mean().round(2))

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
sns.boxplot(data=df, x='online_order', y='rating', ax=ax[0])
ax[0].set_title("Rating by online order (0=No, 1=Yes)")
sns.boxplot(data=df, x='book_table', y='rating', ax=ax[1])
ax[1].set_title("Rating by table booking (0=No, 1=Yes)")
save("q4_online_booking_ratings")

# ---------- Q5: Statistical test ----------
section("Q5. T-TEST (online order vs rating)")
a = df[df.online_order == 1]['rating']
b = df[df.online_order == 0]['rating']
t, p = stats.ttest_ind(a, b, equal_var=False)
print(f"Mean with online order: {a.mean():.3f} | without: {b.mean():.3f}")
print(f"t = {t:.3f}, p-value = {p:.5f}")
print("Significant difference" if p < 0.05 else "No significant difference")

# ---------- Q6: What makes a restaurant successful? ----------
section("Q6. SUCCESS")
print("Success rate overall:", round(df['successful'].mean() * 100, 1), "%")
print((df.groupby('price_bucket', observed=True)['successful'].mean() * 100).round(1))
print((df.groupby('online_order')['successful'].mean() * 100).round(1))
print((df.groupby('book_table')['successful'].mean() * 100).round(1))

# Correlation heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(df[['rating', 'cost', 'votes', 'online_order', 'book_table', 'num_cuisines']].corr(),
            annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation heatmap")
save("q6_correlation_heatmap")

# Rating distribution
plt.figure(figsize=(7, 4))
sns.histplot(df['rating'], bins=25, kde=True, color="#e23744")
plt.title("Distribution of ratings")
save("rating_distribution")

print("\nEDA complete. Check the charts/ folder.")