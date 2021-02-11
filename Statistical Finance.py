import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

# NEED TO RENAME THESE PARAMETERS TO BE MORE INSIGHTFUL
# COULD WE MAKE A CLASS CALLED __stat_fin__ THAT CAN HOUSE THESE DEFINITIONS? OR IS THAT TOO MUCH

def pull_data(list, data_frame):
    """Pulls stock data"""

    for l in list:
        data_frame[l] = pdr.DataReader(l.upper(), data_source='yahoo', \
            start='2018-1-1')['Adj Close']


def normalize(data_frame):
    """Normalizes stock data and shows % return over a period of time"""

    normalized_data = (data_frame / data_frame.iloc[0]) * 100
    normalized_data.plot(figsize = (15, 10))
    plt.suptitle('Historical Return of Your Portfolio\'s Stocks', fontsize=20, y=.95)
    plt.show()


def stock_returns(data_table):
    """Calculates the daily return of each stock and puts it into a Data Table"""

    return (data_table / data_table.shift(1)) - 1


def hist_return(returns):
    """Calculates the average return of each stock in the data table and 
    annualizes it based on # of trading days"""

    return returns.mean() * 250


def pfolio_avg_return(returns, weights):
    """Calculates the dot product of each stocks' weights against 
    its respective annual avg return"""

    return np.dot(weights, hist_return(returns))


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


# creates an empty data frame for use when pulling data
data = pd.DataFrame()

# gathers inputs for the data frame and formats them appropriately

while True:

    tickers = input('Please input the ticker of each stock in your portfolio: ') \
        .upper().replace(',', '').split(' ')

    print(tickers)

    # confirmation of the inputs to ensure correct formatting/spelling
    confirmation = input('Please confirm that the above tickers comprise your entire portfolio using Y / N: ') \
        .upper()

    
    if confirmation == 'N':
        
        greeting = input('Please restart the program.')
        
    else:

        '''sets up an empty dictionary so that we can easily
        reference and assign weights to a ticker'''
        pfolio_fmv = {}

        # loop that assigns the market value to each stock in the portfolio
        for t in tickers:
            ques_wghts = input(f'Please input the dollar market value of your investment in {t}: $')
            pfolio_fmv[t] = float(ques_wghts)
        
        weights = wghts_calc(pfolio_fmv)

        print(weights)

        # NEED TO FIGURE THIS OUT - TRYING TO ASSIGN THE WEIGHTS TO EACH TICKER BUT ONLY PRINTS ONE WEIGHT TO ALL TICKERS
        pretty_weights = {}
        for t in tickers:
            pretty_weights[t] = pd.DataFrame(weights)

        print(pretty_weights)

        pull_data(tickers, data)

        # converts all NaNs to 0
        data.fillna(0)

        normalize(data)

        print('EXPECTED RETURN OF PORTFOLIO')

        # calculates the expected return for a portoflio
        returns = stock_returns(data)
        avg_return = pfolio_avg_return(returns, weights)
        avg_return = str(round(avg_return * 100,2))
        print(f'The expected return of your portfolio based on historical averages is {avg_return}%')
    
        print('CORRELATION OF RETURNS FOR STOCKS IN YOUR PORTFOLIO')
        
        # calculates the correlation of each stock in the portfolio
        corr = returns.corr()
        print(corr)

        print('STANDARD DEVIATION OF YOUR PORTFOLIO')

        '''calculates the covariance of each stock for use when calculating
        the portfolio's standard deviation'''
        cov = returns.cov() * 250

        # calculates the standard deviation of a portfolio
        pfolio_sd = str(round(std_dev(weights, cov) * 100, 2))
        print(f'The standard deviation of your portfolio is {pfolio_sd}%')

        print('REMAINING DIVERSIFIABLE RISK IN YOUR PORTFOLIO')

        # CONTINUE WRITING PROGRAM HERE
        # OTHER IDEAS - show how the std dev compares to that of the S&P 500
