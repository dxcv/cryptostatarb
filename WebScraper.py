import pandas as pd

# Reads in the index list "100 List.csv"
summary = pd.read_csv('./Data/top_cryptos.csv')
cols_to_drop = ['Price', 'Circulating Supply', 'Volume (24h)', 'Change (24h)', 'Price Graph (7d)']
summary.drop(cols_to_drop, inplace=True, axis=1)
count = 1

# Download data for top 100 cryptos by market cap from April 28, 2013 to April 24, 2018
# We use read_html which uses Beautiful Soup to scrap data of coinmarketcap.com and dump it into a .csv file
for i in summary['Name']:
    df = pd.read_html('https://coinmarketcap.com/currencies/' + i + '/historical-data/?start=20130428&end=20180424')
    crypto = pd.DataFrame(df[0])
    crypto['Date'] = pd.to_datetime(crypto.Date)
    crypto.sort_values(by='Date', ascending=True, inplace=True)
    crypto.set_index('Date', inplace=True)
    crypto.to_csv(i + '.csv')
