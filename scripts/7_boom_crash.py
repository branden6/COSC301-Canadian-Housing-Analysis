# boom and crash labeling
# uses the year-over-year change to flag years where prices spiked or dropped a lot
# a boom is defined as yoy change > 15% and a crash is yoy change < -5%
# these thresholds are just reasonable starting points based on what we see in the data

import pandas as pd
import sqlite3

with sqlite3.connect('data/housing_data.db') as conn:
    df = pd.read_sql('SELECT * FROM yoy_change', conn) # using the yoy_change table from the previous script

# label each row
def label_event(change):
    if change > 15:
        return 'Boom'
    elif change < -5:
        return 'Crash'
    else:
        return 'Stable'

df['event'] = df['yoy_change'].apply(label_event)

# just pull out the boom and crash rows
events = df[df['event'] != 'Stable'][['geo', 'ref_date', 'year', 'month', 'value', 'yoy_change', 'event']]
events = events.sort_values('yoy_change', ascending=False)

print(f"\nTotal boom months found: {len(events[events['event'] == 'Boom'])}")
print(f"Total crash months found: {len(events[events['event'] == 'Crash'])}")

print("\nSample booms:\n")
print(events[events['event'] == 'Boom'].head(10).to_string(index=False))

print("\nSample crashes:\n")
print(events[events['event'] == 'Crash'].head(10).to_string(index=False))

# save full labeled dataset (including stable) to db and csv
with sqlite3.connect('data/housing_data.db') as conn:
    df.to_sql('boom_crash_labels', conn, if_exists='replace', index=False)

df.to_csv('data/7_boom_crash_labels.csv', index=False)

print("\nDone. Boom/crash labels saved to db and data/7_boom_crash_labels.csv")
