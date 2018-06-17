import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


class Backtest:

    def __init__(self, commission, start_date, end_date):
        self.commission = commission
        self.start_date = start_date
        self.end_date = end_date

    def get_start_end_index(self, data, window_ols):
        start_date_dt = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
        end_date_dt = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")

        start_id = data[data['date'] == start_date_dt].index[0]

        end_id = data[data['date'] == end_date_dt].index[0]

        if start_id < window_ols:
            start_id = window_ols

        if end_id > (len(data.index) - window_ols):
            end_id = (len(data.index) - window_ols)

        return start_id, end_id

    def run_backtest(self, trader, strategy, data, tester, ols_window):

        start_id, end_id = self.get_start_end_index(data.currencies, ols_window)

        # Time series plot
        plt.figure()
        plt.title(data.name1 + ', ' + data.name2 + ' Time Series')
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.semilogy(data.currencies[data.name1][start_id:end_id])
        plt.semilogy(data.currencies[data.name2][start_id:end_id])

        for i in range(start_id, end_id):

            # Net positions
            sum_two = np.sum(trader.position2)
            sum_one = np.sum(trader.position1)

            price_one = data.currencies[data.name1][i]
            price_two = data.currencies[data.name2][i]
            hprice_one = data.currencies[data.name1][(i - ols_window):i]
            hprice_two = data.currencies[data.name2][(i - ols_window):i]

            # If we are not trading
            if sum_two == 0 and sum_one == 0 and tester.test_cointegration(hprice_one, hprice_two):

                # Calculate beta
                beta = tester.calculate_beta(hprice_one, hprice_two)

                # Calculate z-score
                zscore = tester.calculate_zscore(hprice_one, hprice_two, beta)

                trader.open_zscore.append(np.nan)
                trader.zscore.append(zscore)
                trader.beta.append(beta)

                # Check trading signal
                value, position_one, position_two = strategy.generate_signal \
                    (zscore, beta, price_one, price_two,
                     sum_one, sum_two, self.commission,
                     trader.value[0] * trader.risk_aversion)

            # If we are trading
            elif abs(sum_two) + abs(sum_one) > 0:

                # If not rebalancing
                if tester.test_stationarity(hprice_one, hprice_two, beta):

                    # Use old beta
                    temp = hprice_two - beta * hprice_one
                    zscore = (price_two - beta * price_one - temp.mean()) / temp.std()

                    trader.open_zscore.append(zscore)
                    trader.zscore.append(np.nan)
                    trader.beta.append(beta)

                    # Check trading signal
                    value, position_one, position_two = strategy.generate_signal \
                        (zscore, beta, price_one, price_two,
                         sum_one, sum_two, self.commission,
                         trader.value[0] * trader.risk_aversion)

                # If rebalancing is required
                elif tester.test_cointegration(hprice_one, hprice_two):

                    # Create new beta
                    beta_new = tester.calculate_beta(hprice_one, hprice_two)
                    zscore = tester.calculate_zscore(hprice_one, hprice_two, beta_new)

                    trader.open_zscore.append(zscore)
                    trader.zscore.append(np.nan)
                    trader.beta.append(beta_new)

                    # Rebalance
                    value, position_one, position_two = strategy.rebalance \
                        (zscore, beta, beta_new, price_one, price_two,
                         sum_one, sum_two, self.commission,
                         trader.value[0] * trader.risk_aversion)

                    beta = beta_new

                # If not cointegrated close positions
                else:

                    value = sum_two * price_two + sum_one * price_one - self.commission * (
                            abs(sum_two * price_two) + abs(sum_one * beta * price_one))
                    position_one = -sum_one
                    position_two = -sum_two
                    trader.zscore.append(0)
                    trader.open_zscore.append(0)
                    trader.beta.append(0)

            # Handle closed positions
            else:

                value = 0
                position_one = 0
                position_two = 0
                trader.zscore.append(0)
                trader.open_zscore.append(0)
                trader.beta.append(0)

            # Update portfolio
            if i == 0:

                trader.value[0] + value

            else:

                trader.value.append(value)

            trader.position1.append(position_one)
            trader.position2.append(position_two)
