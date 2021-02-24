import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

# NEED TO RENAME THESE PARAMETERS TO BE MORE INSIGHTFUL
# COULD WE MAKE A CLASS CALLED __stat_fin__ THAT CAN HOUSE THESE DEFINITIONS? OR IS THAT TOO MUCH


class statfin:
    def pull_data(list, data_frame):
        """Pulls portfolio stock data and assigns it to a Data Frame object"""

        for l in list:
            data_frame[l] = pdr.DataReader(l.upper(), data_source='yahoo',
                                           start='2018-1-1')['Adj Close']

    def normalize(data_frame):
        """Normalizes stock data and shows % return over a period of time"""

        normalized_data = (data_frame / data_frame.iloc[0]) * 100
        normalized_data.plot(figsize=(15, 10))
        plt.suptitle('Historical Return of Your Portfolio\'s Stocks',
                     fontsize=20, y=.95)
        plt.show()

    def stock_returns(data_table):
        """Calculates the daily return of each stock and puts it into a Data Table"""

        return (data_table / data_table.shift(1)) - 1

    def hist_return(data_table):
        """Calculates the average return of each stock in the data table and 
        annualizes it based on # of trading days - not rounded for calculation
        purposes"""

        returns = statfin.stock_returns(data_table)
        return returns.mean() * 250

    def pfolio_avg_return(data_table, weights):
        """Calculates the dot product of each stocks' weights against 
        its respective annual avg return"""

        return round(np.dot(weights, statfin.hist_return(data_table)) * 100, 2)

    def wghts_calc(dict):
        """Calculates the weights of each stock in a portfolio and adds them to an array"""

        x = 0
        weights = []

        for d in dict:
            x += dict[d]
        for d in dict:
            weights.append(dict[d] / x)

        weights = np.array(weights)
        return weights

    def std_dev(weights, covariance):
        """calculates the standard deviation of a portfolio"""

        return round(np.dot(weights.T, np.dot(covariance, weights) ** .5) * 100, 2)


while True:

    # creates an empty data frame pulling data
    data = pd.DataFrame()

    # gathers and formats inputs for the data frame
    tickers = input('Please input the ticker of each stock in your portfolio: ') \
        .upper().replace(',', '').split(' ')

    print(tickers)

    # confirmation of the inputs to ensure correct formatting/spelling
    confirmation = input('Please confirm that the above tickers comprise your entire portfolio using Y / N: ') \
        .upper()

    if confirmation == 'N':
        greeting = input('Please restart the program.\n')

    else:
        # allows user to choose benchmark
        print('Please enter the ticker for the benchmark you\'d like to compare your portfolio against. If you want to use an index, use the following tickers below:\n')
        print('S&P 500: ^GSPC')
        print('DJIA: ^DJI')
        print('Nasdaq: ^IXIC\n')
        benchmark = input().upper().split(' ')

        # formats benchmark naming convention
        if benchmark == '^GSPC':
            bench_name = 'the S&P 500'
        elif benchmark == '^DJI':
            bench_name = 'the Dow Jones Industrial Average'
        elif benchmark == '^IXIC':
            bench_name = 'the NASDAQ'
        else:
            bench_name = benchmark

        # empty dictionary to assign weights to each ticker
        pfolio_fmv = {}

        # assigns market value to each stock in portfolio
        for t in tickers:
            ques_wghts = input(
                f'Please input the dollar market value of your investment in {t}: $')
            pfolio_fmv[t] = float(ques_wghts)

        # calculates weight of each stock in portfolio
        weights = statfin.wghts_calc(pfolio_fmv)

        # assigns each weight to a stock and displays it
        wghts_list = list(weights)
        for w in wghts_list:
            str(round(w * 100, 2)) + '%'
        pretty_weights = dict(zip(tickers, wghts_list))
        print(pretty_weights)

        statfin.pull_data(tickers, data)

        statfin.normalize(data)

        print('PORTFOLIO EXPECTED RETURN VS. THE BROADER MARKET\n')

        # calculates the expected return for a portoflio
        avg_return = str(statfin.pfolio_avg_return(data, weights))

        # pulls benchmark data for portfolio vs. benchmark analysis
        mkt = pdr.DataReader(benchmark, data_source='yahoo',
                             start='2018-1-1')['Adj Close']

        # calculates avg historical return for the benchmark
        mkt_hist_rtrns = str(round(statfin.hist_return(mkt).iloc[0] * 100, 2))

        print(
            f'Your portfolio\'s expected return based on historical averages is {avg_return}% as compared to {bench_name}\'s return of {mkt_hist_rtrns}%.')

        if float(avg_return) < float(mkt_hist_rtrns):
            print('Your portfolio is expected to underperform the market.\n')
        else:
            print('Your portfolio is expected to outperform the market.\n')

        print('PORTFOLIO STANDARD DEVIATION VS. THE BROADER MARKET\n')

        # calculates covariance for use when calculating the portfolio's standard deviation
        returns = statfin.stock_returns(data)
        cov = returns.cov() * 250

        # calculates the standard deviation of a portfolio
        pfolio_sd = str(statfin.std_dev(weights, cov))
        print(f'The standard deviation of your portfolio is {pfolio_sd}%\n')

        mkt_std = str(round((statfin.stock_returns(mkt).std().iloc[0] * 250 ** .5)
                            * 100, 2))
        print(
            f'Your portfolio\'s standard deviation is {pfolio_sd}% as compared to {bench_name}\'s standard deviation of {mkt_std}%.')

        if float(pfolio_sd) < float(mkt_std):
            print('Your portfolio is less risky than the broader market.\n')
        else:
            print('Your portfolio is riskier than the broader market.\n')

        print('CORRELATION OF RETURNS FOR STOCKS IN YOUR PORTFOLIO\n')

        # calculates the correlation of each stock in the portfolio
        correlation = returns.corr()
        print(correlation)
        print()

        print('REMAINING DIVERSIFIABLE RISK IN YOUR PORTFOLIO\n')

        # CONTINUE WRITING PROGRAM HERE

        # OTHER IDEAS:
        # have .csv file that contains ticker, # of shares, and cost / share
        # have code pull this data rather than use inputs
        # weights calc would definitely change with this
        # could calc the total return on portfolio
        # add sharpe ratio
