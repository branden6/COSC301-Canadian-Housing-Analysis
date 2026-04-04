"""
measures how unstable each region's housing market is
uses the standard deviation of year-over-year % change
a higher value means prices swing around more from year to year
"""

import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    df = pd.read_sql('SELECT * FROM yoy_change', conn)

# just in case any missing yoy values
df = df.dropna(subset=['yoy_change']).copy()

#volatility score for each region, renamed to volatility score
volatility_df = df.groupby('geo', as_index=False)['yoy_change'].std()
volatility_df = volatility_df.rename(columns={'yoy_change': 'volatility_score'})

# sort from most volatile to least volatile
volatility_df = volatility_df.sort_values(by='volatility_score', ascending=False)

print("\nTop 10 most volatile regions:\n")
print(volatility_df.head(10).to_string(index=False))

print("\nTop 10 least volatile regions:\n")
print(volatility_df.tail(10).to_string(index=False))

# save to db and csv for tableau outputs on final report
with sqlite3.connect('data/housing_data.db') as conn:
    volatility_df.to_sql('volatility_by_region', conn, if_exists='replace', index=False)

volatility_df.to_csv('data/9_volatility_by_region.csv', index=False)

print("\nDone. Volatility analysis saved to db and data/9_volatility_by_region.csv")