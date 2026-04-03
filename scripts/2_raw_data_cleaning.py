#cleaning script for the housing price index dataset
#loads raw data from sqlite, drops junk columns, fixes types, saves cleaned version
"""
Note:
The NHPI is indexed to December 2016 = 100, meaning values represent relative
price levels rather than absolute housing prices. As a result, long-term comparisons
(e.g., 1981–2024) may not reflect intuitive growth patterns and are used here
for exploratory purposes only.
"""

import pandas as pd
import sqlite3

conn = sqlite3.connect('data/housing_data.db')
df = pd.read_sql('SELECT * FROM raw_housing', conn)
conn.close()

#dropping these columns that we dont need : 
#SYMBOL and TERMINATED are completely empty
#UOM and SCALAR_FACTOR are the same value in every row
#COORDINATE sounds useful but its not lat/lon. its just an internal stats canada series id (like 1.1, 2.3 etc), geo column has the actual region names
#the rest are internal stats canada ids we don't use
cols_to_drop = [
    'SYMBOL', 'TERMINATED',
    'UOM', 'UOM_ID',
    'SCALAR_FACTOR', 'SCALAR_ID',
    'DECIMALS',
    'DGUID',
    'VECTOR', 'COORDINATE'
]
df = df.drop(columns=cols_to_drop)

# rename columns to something readable. left is the raw name and the right is the new name we will use from now on.
df = df.rename(columns={
    'REF_DATE': 'ref_date',
    'GEO': 'geo',
    'New housing price indexes': 'price_category',
    'VALUE': 'value',
    'STATUS': 'status'
})

#convert ref_date and pull out year/month for easier filtering later
df['ref_date'] = pd.to_datetime(df['ref_date'], format='%Y-%m')
df['year'] = df['ref_date'].dt.year
df['month'] = df['ref_date'].dt.month
df['ref_date'] = df['ref_date'].dt.strftime('%Y-%m')

#value comes in as a string, so convert to float
#rows with suppressed/missing data will become NaN which is fine
df['value'] = pd.to_numeric(df['value'], errors='coerce')

#null status just means normal data, make that explicit
#other codes: E = estimate, .. = not available, x = suppressed
df['status'] = df['status'].fillna('normal')

df = df[['ref_date', 'year', 'month', 'geo', 'price_category', 'value', 'status']]

# save to the same db as a new table
conn = sqlite3.connect('data/housing_data.db')
df.to_sql('cleaned_housing', conn, if_exists='replace', index=False)
conn.close()

print('done. cleaned_housing table saved to housing_data.db')
