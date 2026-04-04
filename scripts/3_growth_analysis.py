"""
this script is for long-term changes in the New Housing Price Index for each canadian region
"""
import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    df = pd.read_sql('SELECT * FROM cleaned_housing', conn)

# Filter to total housing prices only
df = df[df['price_category'] == 'Total (house and land)']

# yearly average value for each region
yearly_df = df.groupby(['geo', 'year'], as_index=False)['value'].mean()

# earliest and latest yearly average for each region
first_values = yearly_df.loc[yearly_df.groupby('geo')['year'].idxmin()]
last_values = yearly_df.loc[yearly_df.groupby('geo')['year'].idxmax()]

# Keeping just columns needed for growth
first_values = first_values[['geo', 'year', 'value']].rename(columns={
    'year': 'start_year',
    'value': 'start_value'
})

last_values = last_values[['geo', 'year', 'value']].rename(columns={
    'year': 'end_year',
    'value': 'end_value'
})

# earliest and latest values merged into one table
growth_df = pd.merge(first_values, last_values, on='geo')

# need to remove any regions where growth cant be calculated
growth_df = growth_df.dropna(subset=['start_value', 'end_value'])
growth_df = growth_df[growth_df['start_value'] != 0]

# Calculation for percentage growth from first to last value
growth_df['growth_percent'] = (
    (growth_df['end_value'] - growth_df['start_value']) / growth_df['start_value']
) * 100

# Sort regions from highest growth to lowest
growth_df = growth_df.sort_values(by='growth_percent', ascending=False)

# Print results
print("\nTop 10 regions by long-term housing price growth:\n")
print(growth_df[['geo', 'start_year', 'start_value', 'end_year', 'end_value', 'growth_percent']].head(10))

print("\nBottom 10 regions by long-term housing price growth:\n")
print(growth_df[['geo', 'start_year', 'start_value', 'end_year', 'end_value', 'growth_percent']].tail(10))

# save to db and export csv for tableau
with sqlite3.connect('data/housing_data.db') as conn:
    growth_df.to_sql('growth_by_region', conn, if_exists='replace', index=False)

growth_df.to_csv('data/3_growth_by_region.csv', index=False)

print("\nDone. Growth analysis saved to db and data/3_growth_by_region.csv")