# peak analysis
# for each region, find the all-time high index value and when it happened
# also check if the region is still at its peak or has dropped since
# this tells us which markets are currently overheated vs which have cooled off

import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    df = pd.read_sql('SELECT * FROM cleaned_housing', conn)

# total housing only
df = df[df['price_category'] == 'Total (house and land)'].copy()
df = df.dropna(subset=['value'])

# find the peak value and when it happened for each region
peak_idx = df.groupby('geo')['value'].idxmax()
peaks = df.loc[peak_idx][['geo', 'ref_date', 'year', 'value']].rename(columns={
    'ref_date': 'peak_date',
    'year': 'peak_year',
    'value': 'peak_value'
})

# get the most recent value for each region
latest = df.sort_values('ref_date').groupby('geo').last()[['ref_date', 'value']].rename(columns={
    'ref_date': 'latest_date',
    'value': 'latest_value'
})

# merge together
result = pd.merge(peaks, latest, on='geo')

# how far below the peak is the current value (drawdown)
result['drawdown_pct'] = ((result['latest_value'] - result['peak_value']) / result['peak_value']) * 100

# label whether the region is still at peak or has dropped
def peak_status(row):
    if row['latest_date'] == row['peak_date']:
        return 'At Peak'
    elif row['drawdown_pct'] > -5:
        return 'Near Peak'
    else:
        return 'Below Peak'

result['status'] = result.apply(peak_status, axis=1)

result = result.sort_values('drawdown_pct')

print("\nRegions furthest below their peak:\n")
print(result[result['status'] == 'Below Peak'][['geo', 'peak_date', 'peak_value', 'latest_value', 'drawdown_pct']].to_string(index=False))

print("\nRegions still at or near their peak:\n")
print(result[result['status'] != 'Below Peak'][['geo', 'peak_date', 'peak_value', 'latest_value', 'drawdown_pct']].to_string(index=False))

# save to db and csv
with sqlite3.connect('data/housing_data.db') as conn:
    result.to_sql('peak_analysis', conn, if_exists='replace', index=False)

result.to_csv('data/8_peak_analysis.csv', index=False)

print("\nDone. Peak analysis saved to db and data/8_peak_analysis.csv\n")
