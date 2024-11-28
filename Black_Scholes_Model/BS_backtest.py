import numpy as np
import pandas as pd
from scipy.stats import norm
import yfinance as yf
import matplotlib.pyplot as plt
from BS_model import get_stock_data
from BS_model import black_scholes
from datetime import datetime


def historical_data(ticker, start_date, end_date):
    stock = yf.download(ticker, start=start_date, end=end_date)
    stock['Return'] = stock['Close'].pct_change()

    # estimate volatility as the rolling std of returns over 21 days
    stock['Volatility'] = stock['Return'].rolling(window=21).std() * np.sqrt(252)
    stock.dropna(inplace=True)
    return stock


def BS_backtest(ticker, start_date, end_date, K_multiplier=1.05, option_type= "call", r = 0.05, delta_threshold = 0.02, window = 5):
    data = historical_data(ticker, start_date, end_date)
    data.reset_index(inplace=True)


    initial_price = data['Close'].iloc[0]

    K = initial_price * K_multiplier

    cash = 0
    position = 0
    option_prices = []
    dates = []
    trades = []
    daily_pnl = []
    monthly_pnl = {}
    delta_history = []

    for i in range(len(data)):

        S = data['Close'][i] # current stock price 
        expiration_date = data['Date'][i] + pd.Timedelta(days=30)
        T = (expiration_date - data['Date'][i]).days / 365
        T = (data['Date'].iloc[-1] - data['Date'][i]).days / 365 # time remaining in years until the end date 
        K = S * K_multiplier
        sigma = data['Volatility'][i] # current volatility

        if T <= 0 or np.isnan(sigma):
            daily_pnl.append(cash)
            continue  # carry foward cash if no trade 

        option_price, greeks = black_scholes(S, K, T, r, sigma, option_type)
        option_prices.append(option_price)
        option_prices
        delta = greeks['Delta']
        gamma = greeks['Gamma']
        theta = greeks['Theta']
        vega = greeks['Vega']
        rho = greeks['Rho']
        delta_history.append(delta)

        # Trading logic: Enter or exit position based on delta
        if delta >= 0.5 + delta_threshold and position == 0:  # Enter long
            cash -= option_price
            position = 1
            trades.append((data['Date'][i], "BUY", option_price, K))

        elif delta <= 0.5 - delta_threshold and position == 1:  # Exit long
            cash += option_price
            position = 0
            trades.append((data['Date'][i], "SELL", option_price, K))
            print(trades)

        # Update daily P&L
        daily_pnl.append(cash + position * option_price)
        

        # Track monthly P&L
        month = data['Date'][i].strftime('%Y-%m')  # Format date as "YYYY-MM"
        if month not in monthly_pnl:
            monthly_pnl[month] = 0
        monthly_pnl[month] += daily_pnl[-1] - (daily_pnl[-2] if len(daily_pnl) > 1 else 0)

    # Final P&L
    final_pnl = cash + (position * option_price if position != 0 else 0)

    # Print results
    print(f"Final P&L: ${final_pnl:.2f}")
    print("Monthly Profits:")
    for month, profit in monthly_pnl.items():
        print(f"{month}: ${profit:.2f}")

    # Plot results
    # plt.figure(figsize=(12, 6))
    # plt.plot(data['Date'], daily_pnl, label='Cumulative P&L')
    # plt.axhline(0, color='red', linestyle='--', label='Break-even')
    # plt.xlabel('Date')
    # plt.ylabel('Profit and Loss ($)')
    # plt.title(f'{ticker} Option Trading Strategy P&L (Dynamic Strike)')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    return final_pnl, trades, monthly_pnl

if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2022-01-01"
    end_date = "2022-12-31"
    K_multiplier = 1.05  # Strike price is 105% of initial price
    option_type = "call"  # 'call' or 'put'
    r = 0.05

    BS_backtest(ticker, start_date, end_date, K_multiplier, option_type, r=0.05, delta_threshold=0.01070507813902347)

    
