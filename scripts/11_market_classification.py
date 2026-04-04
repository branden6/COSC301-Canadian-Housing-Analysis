# groups regions into simple categories based on growth and volatility

import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    growth = pd.read_sql('SELECT geo, growth_percent FROM recent_growth_by_region', conn)
    volatility = pd.read_sql('SELECT geo, volatility_score FROM volatility_by_region', conn)
    peak = pd.read_sql('SELECT geo, drawdown_pct FROM peak_analysis', conn)

# merge datasets
df = growth.merge(volatility, on='geo')
df = df.merge(peak, on='geo')

# classification logic
def classify(row):
    if row['growth_percent'] > 25 and row['volatility_score'] > 6:
        return 'High Growth & High Volatility (Risky)'
    elif row['growth_percent'] > 25:
        return 'High Growth & Stable'
    elif row['drawdown_pct'] < -5:
        return 'Declining Market'
    else:
        return 'Moderate Growth (Stable)'

df['market_type'] = df.apply(classify, axis=1)

print("\nMarket classification:\n")
print(df[['geo', 'growth_percent', 'volatility_score', 'drawdown_pct', 'market_type']].to_string(index=False))

# save
with sqlite3.connect('data/housing_data.db') as conn:
    df.to_sql('market_classification', conn, if_exists='replace', index=False)

df.to_csv('data/11_market_classification.csv', index=False)

print("\nDone. Market classification saved.")