import numpy as np
import pandas as pd
from scipy.stats import norm
import yfinance as yf
import matplotlib.pyplot as plt
from Black_Scholes_Model import get_stock_data
from Black_Scholes_Model import black_scholes


def historical_data(ticker, start_date, end_date3):
    stock = yf.download(ticker, start=start_date, end=end_date)
    stock['Return'] = stock['Close'].pct_change()
    stock['Volatility'] = stock['Return'].rolling(window=21).std() * np.sqrt(252)
    stock.dropna(inplace=True)
    return stock


def BS_backtest(ticker, start_date, end_date, K_multiplier=1.05, option_type= "call", r = 0.05):
    data = historical_data(ticker, start_date, end_date)
    data.reset_index(inplace=True)


    initial_price = data['Close'].iloc[0]

    K = initial_price * K_multiplier

    positions = []
    option_prices = []
    dates = []

    for i in range(len(data)):
        S = data['Close'][i]
        T = (data['Date'].iloc[-1] - data['Date'][i]).days / 365
        sigma = data['Volatility'][i]

        if T <= 0 or np.isnan(sigma):
            continue  # Skip invalid data

        option_price, greeks = black_scholes(S, K, T, r, sigma, option_type)
        option_prices.append(option_price)
        dates.append(data['Date'][i])

        # Trading strategy
        if i == 0:
            positions.append(-option_price)  # Buy option
        elif i == len(data) - 1:
            positions.append(option_price)  # Sell option

    if not positions:
        print("No valid positions were generated during the backtest.")
        return

    # Calculate total return
    total_return = sum(positions)
    print(f"Total Return from the {option_type.capitalize()} Option Strategy: ${total_return:.2f}")

    # Plotting
    plt.figure(figsize=(12,6))
    plt.plot(dates, option_prices, label=f'{option_type.capitalize()} Option Price')
    plt.xlabel('Date')
    plt.ylabel('Option Price')
    plt.title(f'{ticker} {option_type.capitalize()} Option Price Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

    return total_return


if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    K_multiplier = 1.05  # Strike price is 105% of initial price
    option_type = "call"  # 'call' or 'put'
    r = 0.05

    BS_backtest(ticker, start_date, end_date, K_multiplier, option_type, r)

    
