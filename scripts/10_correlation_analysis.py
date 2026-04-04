
"""
combines key regional metrics to see how they relate to each other
Answers:
 - do speculative markets grow faster?
 - are high-growth markets more volatile?
 - are regions below peak more volatile?
"""
import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    recent_growth = pd.read_sql('SELECT * FROM recent_growth_by_region', conn)
    land_premium = pd.read_sql('SELECT * FROM land_premium', conn)
    volatility = pd.read_sql('SELECT * FROM volatility_by_region', conn)
    peak = pd.read_sql('SELECT * FROM peak_analysis', conn)

# land premium is monthly, so this summarizes it to one average value per region
land_summary = land_premium.groupby('geo', as_index=False)['land_premium'].mean()
land_summary = land_summary.rename(columns={'land_premium': 'avg_land_premium'})

# keep columns we need
recent_growth = recent_growth[['geo', 'growth_percent']]
volatility = volatility[['geo', 'volatility_score']]
peak = peak[['geo', 'drawdown_pct']]

# merge
merged = recent_growth.merge(land_summary, on='geo', how='inner')
merged = merged.merge(volatility, on='geo', how='inner')
merged = merged.merge(peak, on='geo', how='inner')

print("\nCombined regional metrics:\n")
print(merged.head(10).to_string(index=False))

# correlation 
correlation_matrix = merged[['growth_percent', 'avg_land_premium', 'volatility_score', 'drawdown_pct']].corr()

print("\nCorrelation matrix:\n")
print(correlation_matrix.round(3).to_string())

# summary to test and see results
print("\nKey relationships:\n")
print(f"Growth vs Land Premium: {correlation_matrix.loc['growth_percent', 'avg_land_premium']:.3f}")
print(f"Growth vs Volatility: {correlation_matrix.loc['growth_percent', 'volatility_score']:.3f}")
print(f"Land Premium vs Volatility: {correlation_matrix.loc['avg_land_premium', 'volatility_score']:.3f}")
print(f"Growth vs Drawdown: {correlation_matrix.loc['growth_percent', 'drawdown_pct']:.3f}")

# Saving data for tableau output later on
with sqlite3.connect('data/housing_data.db') as conn:
    merged.to_sql('regional_correlation_metrics', conn, if_exists='replace', index=False)
    correlation_matrix.to_sql('regional_correlation_matrix', conn, if_exists='replace')

merged.to_csv('data/10_regional_correlation_metrics.csv', index=False)
correlation_matrix.to_csv('data/10_regional_correlation_matrix.csv')

print("\nDone. Correlation analysis saved to db and data/10_regional_correlation_*.csv")