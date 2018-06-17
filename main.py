from CryptoData import CryptoData
from Strategy import Strategy
from Backtest import Backtest
from Tracker import Tracker
from Tester import Tester
from Plotter import Plotter

if __name__ == '__main__':

    # Chose pair on which to test trading strategy
    pair = ['BTC', 'ETC']

    # Set rolling window size
    ols_window = 96 * 4  # number of 15 minute periods in four days
    ma_window = 96 * 4
    
    # Trade indicator levels
    zscore_lvl = 1.5
    zscore_close = 0.5

    initial_capital = 100000.0

    # Maximum allowed exposure
    risk_aversion = 0.1

    # Simulated commission
    commission = 0.5 / 100

    # Establish significance level for statistical acceptance
    significance_lvl = 0.3

    # Delineate start and end dates
    start_date = '2018-03-11 10:00:00'
    end_date = '2018-04-24 10:00:00'

    # Set data frame
    df = CryptoData(pair, ols_window, ma_window)

    # Track positions
    trader = Tracker(initial_capital, risk_aversion)

    # Test for cointegration and stationarity, and calculate beta and z-score
    test = Tester(significance_lvl)

    # Establish trading and rebalancing rules
    strategy = Strategy(zscore_lvl, zscore_close)

    # Backtest the strategy between delineated start and end date
    backtest = Backtest(commission, start_date, end_date)

    # Read in data
    df.read_file()

    # Run the backtest
    backtest.run_backtest(trader, strategy, df, test, ols_window)

    # Plot results
    plotter = Plotter()
    plotter.plot(trader, df)
