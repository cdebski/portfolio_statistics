import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import os

# NEED TO FIGURE OUT HOW TO USE OS PACKAGE - COULD BE HELPFUL FOR EVERYONE
# NEED TO RENAME THESE PARAMETERS TO BE MORE INSIGHTFUL

class statfin:
    def pull_data(list, stock_DataFrame):
        """pulls portfolio stock data and assigns it to a Data Frame object"""

        for l in list:
            stock_DataFrame[l] = pdr.DataReader(l.upper(), data_source='yahoo',
                                                start='2018-1-1')['Adj Close']

    def normalize(stock_Data_Frame):
        """normalizes stock data and shows % return over a period of time"""

        normalized_data = (stock_Data_Frame / stock_Data_Frame.iloc[0]) * 100
        normalized_data.plot(figsize=(15, 10))
        plt.suptitle('Historical Return of Your Portfolio\'s Stocks',
                     fontsize=20, y=.95)
        plt.show()

    def stock_returns(stock_DataFrame):
        """calculates the daily return of each stock and puts it into a Data Table"""

        return (stock_DataFrame / stock_DataFrame.shift(1)) - 1

    def hist_return(stock_DataFrame):
        """calculates the average return of each stock in the data table and 
        annualizes it based on # of trading days - not rounded for calculation
        purposes"""

        returns = statfin.stock_returns(stock_DataFrame)
        return returns.mean() * 250

    def pfolio_avg_return(stock_DataFrame, weights):
        """calculates the dot product of each stocks' weights against 
        its respective annual avg return"""

        return round(np.dot(weights, statfin.hist_return(stock_DataFrame)) * 100, 2)

    def wghts_calc(dictionary):
        """calculates the weights of each stock in a portfolio and adds them to an array"""

        x = 0
        weights = []

        for d in dictionary:
            x += dictionary[d]
        for d in dictionary:
            weights.append(dictionary[d] / x)

        weights = np.array(weights)
        return weights

    def pfolio_var(weights, covariance):
        """calculates variance of a portfolio"""

        return np.dot(weights.T, np.dot(covariance, weights))

    def std_dev(weights, covariance):
        """calculates standard deviation of a portfolio"""

        return round(statfin.pfolio_var(weights, covariance) ** .5 * 100, 2)

    def variance(stock_DataFrame):
        """calculates variance for stocks in a portfolio"""

        return stock_DataFrame.var() * 250

    def diversifiable_risk(weights, covariance, stock_DataFrame):
        """calculates diversifiable risk left in a portfolio - not
        rounded for calculation purposes"""

        stox_wghtd_var = 0
        for ticker in stock_DataFrame:
            for index in enumerate(weights):
                stox_wghtd_var += (weights[index] ** 2 *
                                   statfin.variance(stock_DataFrame)[ticker])

        return statfin.pfolio_var(weights, covariance) - stox_wghtd_var

    def non_divers_risk(weights, covariance, stock_DataFrame):
        """calculates non-diversifiable risk in a portfolio"""

        return round(statfin.pfolio_var(weights, covariance) -
                     statfin.diversifiable_risk(
                         weights, covariance, stock_DataFrame)
                     * 100, 2)

    def format(function):
        """formats function as string that is a percentage 
        multiplied by 100 rounded to two decimals ('xx.yy')"""

        return str(round(function * 100, 2))



while True:
    # pulls stock data from csv file
    stock_data = pd.read_csv('C:/Users/Charl/Desktop/data.csv')

    print(stock_data)
    print('')
    
    # confirms that stock data is correct
    confirmation = input('Is the above stock information correct? Use Y / N to answer: \n')

    if confirmation == 'N':
        greeting = input('Please update the .csv saved on your desktop and restart the program.\n')

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
        stock_weights = statfin.wghts_calc(pfolio_fmv)

        # assigns each weight to a stock and displays it
        wghts_list = list(stock_weights)
        for w in wghts_list:
            str(round(w * 100, 2)) + '%'
        pretty_weights = dict(zip(tickers, wghts_list))
        print(pretty_weights)

        statfin.pull_data(tickers, stock_data)

        statfin.normalize(stock_data)

        print('PORTFOLIO EXPECTED RETURN VS. THE BROADER MARKET\n')

        # calculates the expected return for a portoflio
        avg_return = str(statfin.pfolio_avg_return(stock_data, stock_weights))

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
        returns = statfin.stock_returns(stock_data)
        cov = returns.cov() * 250

        # calculates the standard deviation of a portfolio
        pfolio_sd = str(statfin.std_dev(stock_weights, cov))
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

        # NEED TO TEST THESE FUNCTIONS
        pfolio_dr = str(round(statfin.diversifiable_risk(
                              stock_weights, cov, stock_data) * 100, 2))
        print(
            f'The remaining risk in your portfolio that can be diversified is {pfolio_dr}%.\n')

        print('NON-DIVERSIFIABLE RISK IN YOUR PORTFOLIO\n')

        pfolio_ndr = str(statfin.non_divers_risk(stock_weights, cov, stock_data))

        # OTHER IDEAS:
        # have .csv file that contains ticker, # of shares, and cost / share
        # have code pull this data rather than use inputs
        # weights calc would definitely change with this
        # could calc the total return on portfolio
        # add sharpe ratio
