#Land premium analysis

# a house price is made up of two parts: the land it sits on + the actual building.
#this script figures out how much of the price is driven by land vs the building.

#if land prices are rising way faster than house prices, it means people are
#buying for the land (speculation/investment), not just to live there.
# we call this a high "land premium".

# if house prices are rising faster, its more about construction costs / demand
#  for housing itself - more stable, less speculative.

# we calculate: land_index / house_index for each region each month.
#   - ratio > 1 means land is more expensive relative to the house (speculative)
#   - ratio < 1 means the building itself is the main cost (stable)

# we then label each region/month as:
#   High Speculation   - ratio > 1.2
#   Moderate           - ratio between 0.8 and 1.2
#   House-Driven      - ratio < 0.8

import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    df = pd.read_sql('SELECT * FROM cleaned_housing', conn)

# split into the three categories so we can compare them side by side
house = df[df['price_category'] == 'House only'][['ref_date', 'year', 'month', 'geo', 'value']].rename(columns={'value': 'house_index'})
land = df[df['price_category'] == 'Land only'][['ref_date', 'geo', 'value']].rename(columns={'value': 'land_index'})

# join land and house on region + date
merged = pd.merge(house, land, on=['ref_date', 'geo'])

# drop rows where either index is missing (suppressed regions/dates)
merged = merged.dropna(subset=['house_index', 'land_index'])
merged = merged[merged['house_index'] != 0]

# the actual land premium calculation
merged['land_premium'] = merged['land_index'] / merged['house_index']

# label each row based on how speculative the ratio is
def label_premium(ratio):
    if ratio > 1.2:
        return 'High Speculation'
    elif ratio < 0.8:
        return 'House-Driven'
    else:
        return 'Moderate'

merged['label'] = merged['land_premium'].apply(label_premium)

# sort by date then region
merged = merged.sort_values(['year', 'month', 'geo']).reset_index(drop=True)

# quick summary: most recent year average per region
latest_year = merged['year'].max()
summary = merged[merged['year'] == latest_year].groupby('geo')[['land_premium']].mean().round(3)
summary['label'] = summary['land_premium'].apply(label_premium)
summary = summary.sort_values('land_premium', ascending=False)

print(f"\nLand premium by region (avg {latest_year}):\n")
print(summary.to_string())

# save to db and export csv for tableau
with sqlite3.connect('data/housing_data.db') as conn:
    merged.to_sql('land_premium', conn, if_exists='replace', index=False)

merged.to_csv('data/5_land_premium.csv', index=False)

print("\nDone. Land premium saved to db and data/5_land_premium.csv")
