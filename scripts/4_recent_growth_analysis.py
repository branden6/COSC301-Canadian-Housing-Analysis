"""
This script analyzes recent (2020-2024) growth in new housing prices across Canadian regions.
"""

import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    df = pd.read_sql('SELECT * FROM cleaned_housing', conn)

# Filter to total housing prices
df = df[df['price_category'] == 'Total (house and land)'].copy()

# period of 2020-2024
df = df[df['year'] >= 2020]

# yearly averages
yearly_df = df.groupby(['geo', 'year'], as_index=False)['value'].mean()

# 2020 values
start_values = yearly_df[yearly_df['year'] == 2020].rename(columns={
    'value': 'start_value'
})

# 2024 values
end_values = yearly_df.loc[yearly_df.groupby('geo')['year'].idxmax()].rename(columns={
    'year': 'end_year',
    'value': 'end_value'
})

# Merge the values of start and end
growth_df = pd.merge(start_values[['geo', 'start_value']], end_values[['geo', 'end_year', 'end_value']], on='geo')


# Compute growth
growth_df['growth_percent'] = (
    (growth_df['end_value'] - growth_df['start_value']) / growth_df['start_value']
) * 100

# Sort
growth_df = growth_df.sort_values(by='growth_percent', ascending=False)

# Print
print("\nTop 10 regions by recent growth (2020–2024):\n")
print(growth_df[['geo', 'start_value', 'end_value', 'growth_percent']].head(10))

print("\nBottom 10 regions by recent growth:\n")
print(growth_df[['geo', 'start_value', 'end_value', 'growth_percent']].tail(10))

# save to db and export csv for tableau
with sqlite3.connect('data/housing_data.db') as conn:
    growth_df.to_sql('recent_growth_by_region', conn, if_exists='replace', index=False)

growth_df.to_csv('data/4_recent_growth_by_region.csv', index=False)

print("\nDone. Recent growth analysis saved to db and data/4_recent_growth_by_region.csv")