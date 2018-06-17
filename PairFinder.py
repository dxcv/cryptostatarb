import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import coint


# Identify cointegrated pairs
def cointegrated_pairs(data):
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []

    for i in range(n):
        for j in range(i + 1, n):

            series_one = data[keys[i]]
            series_two = data[keys[j]]
            result = coint(series_one, series_two)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.005:
                pairs.append((keys[i], keys[j]))

    return score_matrix, pvalue_matrix, pairs


if __name__ == '__main__':

    num_cryptos = 99
    pairs_data_file = './Data/pairs.csv'
    top_list = pd.read_csv('./Data/top_cryptos.csv')
    top_list = top_list.drop(
        ['#', 'Market Cap', 'Price', 'Circulating Supply', 'Volume (24h)', 'Change (24h)', 'Price Graph (7d)'], axis=1)
    currencies = []
    counter = 0

    for i in range(0, num_cryptos):

        temp = pd.read_csv('./Data/daily_data/' + str(top_list['Name'][i]) + '.csv')

        # Ensure there are at least 1000 days of data to test for cointegration
        if len(temp.index) > 1000:
            print(str(top_list['Name'][i]))
            temp = temp.drop(['Open', 'High', 'Low', 'Volume', 'Market Cap'], axis=1)
            temp['Date'] = pd.to_datetime(temp['Date'], infer_datetime_format=True)
            temp = temp.set_index('Date')

            # Sample daily
            temp = temp.resample('D').mean()
            currencies.append(temp)
            counter = counter + 1

    num_cryptos = counter

    for i in range(0, num_cryptos):
        currencies[i] = currencies[i].rename(columns={'Close': str(top_list['Name'][i])})

    currencies = pd.concat(currencies, axis=1)
    currencies = currencies.dropna(axis=0)
    column_names = currencies.keys()

    keys = currencies.keys()
    scores, pvalues, pairs = cointegrated_pairs(currencies)

    print(pairs)

    sns.heatmap(pvalues, xticklabels=keys.tolist(), yticklabels=keys.tolist(), cmap='RdYlGn_r', mask=(pvalues > 0.8))

    plt.show()

    with open(pairs_data_file, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(pairs)