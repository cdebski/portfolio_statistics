import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

# NEED TO RENAME THESE PARAMETERS TO BE MORE INSIGHTFUL
# COULD WE MAKE A CLASS CALLED __stat_fin__ THAT CAN HOUSE THESE DEFINITIONS? OR IS THAT TOO MUCH


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
    annualizes it based on # of trading days"""

    returns = stock_returns(data_table)
    return returns.mean() * 250


def pfolio_avg_return(data_table, weights):
    """Calculates the dot product of each stocks' weights against 
    its respective annual avg return"""

    return np.dot(weights, hist_return(data_table))


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

    return np.dot(weights.T, np.dot(covariance, weights))


while True:

    # creates an empty data frame for use when pulling data
    data = pd.DataFrame()

    # gathers inputs for the data frame and formats them appropriately
    tickers = input('Please input the ticker of each stock in your portfolio: ') \
        .upper().replace(',', '').split(' ')

    print(tickers)

    # confirmation of the inputs to ensure correct formatting/spelling
    confirmation = input('Please confirm that the above tickers comprise your entire portfolio using Y / N: ') \
        .upper()

    if confirmation == 'N':

        greeting = input('Please restart the program.\n')

    else:

        '''sets up an empty dictionary so that we can easily
        reference and assign weights to a ticker'''
        pfolio_fmv = {}

        # loop that assigns the market value to each stock in the portfolio
        for t in tickers:
            ques_wghts = input(
                f'Please input the dollar market value of your investment in {t}: $')
            pfolio_fmv[t] = float(ques_wghts)

        # calculates the weight of each stock in the portfolio
        weights = wghts_calc(pfolio_fmv)

        # assigns each weight to a stock and displays it
        wghts_list = list(weights)
        for w in wghts_list:
            str(round(w * 100, 2)) + '%'
        pretty_weights = dict(zip(tickers, wghts_list))
        print(pretty_weights)

        pull_data(tickers, data)

        # converts all NaNs to 0
        data.fillna(0)

        normalize(data)

        print('PORTFOLIO EXPECTED RETURN VS. THE BROADER MARKET\n')

        # calculates the expected return for a portoflio
        avg_return = str(round(pfolio_avg_return(data, weights) * 100, 2))

        # pulls S&P 500 data for portfolio vs. market analysis
        mkt = pdr.DataReader('^GSPC', data_source='yahoo',
                             start='2018-1-1')['Adj Close']

        # calculates avg historical return for the market
        mkt_hist_rtrns = str(round(hist_return(mkt) * 100, 2))

        print(
            f'Your portfolio\'s expected return based on historical averages is {avg_return}% as compared to the broader market\'s return of {mkt_hist_rtrns}%.')

        if float(avg_return) < float(mkt_hist_rtrns):
            print('Your portfolio is expected to underperform the market.\n')
        else:
            print('Your portfolio is expected to outperform the market.\n')

        print('STANDARD DEVIATION OF YOUR PORTFOLIO\n')

        '''calculates the covariance of each stock for use when calculating
        the portfolio's standard deviation'''
        returns = stock_returns(data)
        cov = returns.cov() * 250

        # calculates the standard deviation of a portfolio
        pfolio_sd = str(round(std_dev(weights, cov) * 100, 2))
        print(f'The standard deviation of your portfolio is {pfolio_sd}%\n')

        print('PORTFOLIO STANDARD DEVIATION VS. THE BROADER MARKET\n')

        # NEED TO CHECK THE STANDARD DEVIATION CALC FOR BOTH THE MARKET & PFOLIO - MIGHT BE RIGHT/WRONG
        mkt_std = str(round((mkt.std() * 250 ** .5) * 100, 2))
        print(f'Your portfolio\'s standard deviation is {pfolio_sd}% as compared to the broader market\'s standard deviation of {mkt_std}%.')

        if float(pfolio_sd) < float(mkt_std):
            print('Your portfolio is less risky than the broader market.\n')
        else:
            print('Your portfolio is riskier than the broader market.\n')

        print('CORRELATION OF RETURNS FOR STOCKS IN YOUR PORTFOLIO\n')

        # calculates the correlation of each stock in the portfolio
        corr = returns.corr()
        print(corr)
        print()

        print('REMAINING DIVERSIFIABLE RISK IN YOUR PORTFOLIO\n')

        # CONTINUE WRITING PROGRAM HERE
        # OTHER IDEAS - show how the std dev compares to that of the S&P 500
