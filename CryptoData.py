import pandas as pd


class CryptoData:

    def __init__(self, cryptos, ols_window, ma_window):

        self.cryptos = cryptos
        self.ols_window = ols_window
        self.ma_window = ma_window
        self.currencies = []

    # Function ro read 15 minute .csv files and clean data
    def read_file(self):

        for i in range(0, 2):
            tmp = pd.read_csv('./Data/15_min_data/' + str(self.cryptos[i]) + '.csv')
            tmp = tmp.drop(['open', 'high', 'low', 'quoteVolume', 'volume', 'weightedAverage'], axis=1)
            tmp['date'] = pd.to_datetime(tmp['date'], infer_datetime_format=True)
            tmp = tmp.set_index('date')
            tmp = tmp.resample('15T').mean()
            self.currencies.append(tmp)

        for i in range(0, 2):
            self.currencies[i] = self.currencies[i].rename(columns={'close': str(self.cryptos[i])})

        self.currencies = pd.concat(self.currencies, axis=1)
        self.currencies = self.currencies.dropna(axis=0)
        self.currencies = self.currencies.reset_index()
        keys = self.currencies.keys()

        self.name1 = keys[1]
        self.name2 = keys[2]