import io
from datetime import date, datetime, timedelta

import pandas as pd
import requests
from nsepython import *

# today = date.today()
# today = datetime.strftime(today, "%d-%m-%Y")
# df_bh = get_bhavcopy(today)

# print(df_bh)


# url = 'https://nsearchives.nseindia.com/web/sites/default/files/inline-files/MCAP31032023_0.xlsx'
# s = requests.get(url).content
# print(s)
df = pd.read_excel("NSElist.xlsx")

fund_df = pd.read_csv("Multi Cap Fund_company_counts.csv")

# print(df)

# Extract the first word from each Company Name in fund_df
fund_df['First Word'] = fund_df['Company Name'].str.split().str[0]

print(fund_df['First Word'])

df['Company Name'] = df['Company Name'].fillna('')


# Initialize an empty list to store the symbols
symbols = []

# Iterate over each row in fund_df
for index, row in fund_df.iterrows():
    # Get the first word of the Company Name
    first_word = row['First Word']
    
    # Search for a match in the Company Name column of df
    match = df[df['Company Name'].str.contains(first_word, case=False)]
    
    # If a match is found, store the symbol in the symbols list
    if not match.empty:
        symbol = match['Symbol'].values[0]
    else:
        symbol = None
    symbols.append(symbol)

# Add the symbols column to fund_df
fund_df['Symbol'] = symbols
# Remove the 'First Word' column from fund_df
fund_df = fund_df.drop('First Word', axis=1)

# Save the modified fund_df with the same name
fund_df.to_csv("Multi Cap Fund_company_counts.csv", index=False)



