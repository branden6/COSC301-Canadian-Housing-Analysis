import pandas as pd
import sqlite3

#this script reads the raw data from the csv file and creates a sqlite database with a table called 'raw_housing' to store the data.

raw_data = pd.read_csv('data/housing_price_indexes.csv')

conn = sqlite3.connect('data/housing_data.db')

raw_data.to_sql('raw_housing', conn, if_exists='replace', index=False)

conn.close()

print("done. database created and raw data inserted.")