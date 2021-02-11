from pandas_datareader import data as wb
import matplotlib.pyplot as plt


def profit(stock, cost):
    """Calculates the dollar profit / loss in a stock"""

    return float(stock - cost)


def return_per_share(stock, cost):
    """Calculates the % return on an investment"""

    return float((stock - cost) / cost)


def return_on_investment(gain_or_loss, num_shares):
    """Calculates the total profit / loss on the entire investment"""

    return gain_or_loss * num_shares


def stock_data(symbol):
    """Pulls the most recent stock price for the provided ticker"""

    data_frame = wb.DataReader(symbol, data_source='yahoo', start='2000-1-1')['Adj Close']
    return data_frame.iloc[-1]


def stock_chart(symbol):
    """Pulls the last 5 prices for the provided ticker and plots a chart of it"""

    data_frame = wb.DataReader(symbol, data_source='yahoo', start='2000-1-1')['Adj Close']
    data_frame.iloc[-15:].plot(figsize=(10, 10))
    return plt.show()


def pl_analysis(symbol, percent_gain):
    """Calculates the take profit price for the provided ticker based on the desired return"""

    return symbol * (1 + percent_gain)


print('Welcome! Would you like to perform profit / loss analysis?')

while True:
    selection = input('Please enter Y/N: ').upper()

    if selection != 'Y':
        print('Would you like to calculate a "Take Profit" price?')
        selection_2 = input('Please enter Y/N: ').upper()

        if selection_2 != 'Y':
            print('Thank you for using this program!')
            print('Would you like to perform profit / loss analysis?')
        else:
            ticker = input('Please input the ticker of the company you\'d like to analyze: ').upper()

            stock_price = stock_data(ticker)
            print(f'The current stock price of {ticker} is: ${stock_price:,.4}')

            print(f'Please see the chart of the last 15 trading days for {ticker}:')
            stock_chart(ticker)

            gain = float(input('Please input the % gain where you will take profits: '))

            # converts a whole number into a decimal if needed
            if gain >= 1:
                gain = gain / 100
            else:
                pass

            take_profit = pl_analysis(stock_price, gain)
            print(f'Your Take Profit price for {ticker} is ${take_profit:,.4}')
            print('Thank you for using this program!')
            print('Would you like to perform profit / loss analysis?')
    else:
        ticker = input('Please input the ticker of the company you\'d like to analyze: ').upper()
        cost_per_share = int(input('Please input your cost per share: '))
        shares = int(input('Please input the number of shares held: '))

        stock_price = stock_data(ticker)
        print(f'The current stock price of {ticker} is ${stock_price:,.4}')

        # rounds the profit calculation
        profit = round(profit(stock_price, cost_per_share), 4)
        print(f'Your profit per share for {ticker} is ${profit:,.4}')

        # rounds the total profit calculation
        total_profit = round(return_on_investment(profit, shares), 4)
        print(f'Your total profit / loss in {ticker} is ${total_profit:,.4}')

        # formats the return on investment calculation
        roi = return_per_share(stock_price, cost_per_share)
        print(f'Your total profit / loss in {ticker} as a percentage is {roi:,.2%}')
        print('Would you like to perform another profit / loss analysis?')
