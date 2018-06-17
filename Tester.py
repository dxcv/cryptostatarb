from statsmodels.tsa.stattools import coint
import statsmodels.tsa.stattools
import statsmodels.api as sm


class Tester:

    def __init__(self, s):
        self.significance = s

    # Test for cointegration, used for rebalancing
    def test_cointegration(self, coin_one, coin_two):

        if coint(coin_one, coin_two)[1] < self.significance:

            return True

        else:

            return False

    # Test for stationarity via ADF
    def test_stationarity(self, coin_one, coin_two, beta):

        temp = coin_two - beta * coin_one

        if statsmodels.tsa.stattools.adfuller(temp)[1] < self.significance:

            return True

        else:

            return False

    # Calculation of beta via OLS
    @staticmethod
    def calculate_beta(coin_one, coin_two):

        coin_two = coin_two
        coin_one = sm.add_constant(coin_one)
        model = sm.OLS(coin_two, coin_one)
        results = model.fit()
        beta = results.params[1]

        return beta

    # Calculate normalized z-score
    def calculate_zscore(self, coin_one, coin_two, beta):

        spread = coin_two - beta * coin_one
        self.spread_mavg = spread.mean()
        self.spread_std = spread.std()
        zscore = (spread - self.spread_mavg) / self.spread_std

        return zscore.tolist()[-1]
