# year over year change analysis
# for each region, compare this month's index to the same month last year
# this tells us which years had the biggest jumps and which regions are most volatile

import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    df = pd.read_sql('SELECT * FROM cleaned_housing', conn)

# only looking at total housing prices
df = df[df['price_category'] == 'Total (house and land)'].copy()

# sort so the shift works correctly
df = df.sort_values(['geo', 'year', 'month']).reset_index(drop=True)

# for each region, shift the value by 12 months to get last years value
df['value_last_year'] = df.groupby('geo')['value'].shift(12)

# calculate the % change from last year
df['yoy_change'] = ((df['value'] - df['value_last_year']) / df['value_last_year']) * 100

# drop rows where we dont have last year's data (first year of each region)
df = df.dropna(subset=['yoy_change'])

# quick look at biggest single year jumps across all regions
print("\nTop 10 biggest year-over-year increases:\n")
top = df.nlargest(10, 'yoy_change')[['geo', 'ref_date', 'value', 'yoy_change']]
print(top.to_string(index=False))

print("\nTop 10 biggest year-over-year drops:\n")
bottom = df.nsmallest(10, 'yoy_change')[['geo', 'ref_date', 'value', 'yoy_change']]
print(bottom.to_string(index=False))

# save to db and csv for tableau
with sqlite3.connect('data/housing_data.db') as conn:
    df.to_sql('yoy_change', conn, if_exists='replace', index=False)

df.to_csv('data/6_yoy_change.csv', index=False)

print("\nDone. Year-over-year change saved to db and data/6_yoy_change.csv")
