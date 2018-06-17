import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Plotter:

    @staticmethod
    def plot_zscore(zscore, coin_one, coin_two):

        plt.figure()
        plt.plot(zscore)
        plt.title(coin_one + ', ' + coin_two + ' Normalized Spread ')
        plt.ylabel('z-score')
        plt.axhline(0, color='black')
        plt.axhline(1.5, color='#EF8B21', linestyle='--')
        plt.axhline(-1.5, color='#6F9A48', linestyle='--')

    @staticmethod
    def plot_returns(value, coin_one, coin_two):

        tt = 96 * 10
        returns = []
        for i in range(tt, len(value) - tt):
            returns.append((np.sum(value[0:tt + i]) - np.sum(value[0:i])) / np.sum(value[0:i]) * 100.0)
        return_s = pd.Series(returns)

        plt.figure()
        plt.plot(return_s)
        plt.title(coin_one + ', ' + coin_two + ' Percent Returns')
        plt.ylabel('% Returns')

    @staticmethod
    def plot_pnl(value, coin_one, coin_two):

        plt.figure()
        plt.plot(np.cumsum(value))
        plt.title(coin_one + ', ' + coin_two + ' Profit and Loss')
        plt.ylabel('Portfolio Value')

    @staticmethod
    def plot_open_position(position_one, position_two, coin_one, coin_two):

        plt.figure()
        plt.plot(np.cumsum(position_one))
        plt.plot(np.cumsum(position_two))
        plt.legend([str(coin_one), str(coin_two)])
        plt.title(coin_one + ', ' + coin_two + ' Portfolio Positions')
        plt.ylabel('Number of Coins')

    def plot(self, trader, data):

        self.plot_zscore(trader.zscore, data.name1, data.name2)
        self.plot_open_position(trader.position1, trader.position2, data.name1, data.name2)
        self.plot_pnl(trader.value, data.name1, data.name2)
        self.plot_returns(trader.value, data.name1, data.name2)

        plt.show()
