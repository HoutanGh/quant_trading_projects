import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import random as rd
from sklearn.model_selection import train_test_split

global colorlist
colorlist = ['#5398d9',
             '#d75b66',
             '#edd170',
             '#02231c',
             'k']

def monte_carlo(data, test_size, simulations):
    
    # train_test split and handling close price
    
    train, test = train_test_split(data, test_size=test_size, shuffle=False)
    forecast_horizon = len(test)

    train = train.loc[:, ['Close']]

    # log return and drift

    log_return = np.log(train['Close'].iloc[1:] / train['Close'].shift(1).iloc[1:])
    
    drift = (log_return.mean() - log_return.var()) / 2

    pred_time_series = {}

    # geometric brownian motion

    for i in range(simulations):
        pred_time_series[i] = [train['Close'].iloc[0]]

        for j in range(len(train) + forecast_horizon - 1):
            std_returns = drift + log_return.std() * rd.gauss(0, 1)
            
            GBM = pred_time_series[i][-1] * np.exp(std_returns)

            pred_time_series[i].append(GBM.item())
    
    # go through simluations again and pick best one
    # calcualtes the standard deviation between each simulated price path and actual historical prices (df['Close'])
    std = float('inf')
    best = 0
    for i in range(simulations):
        std_sim = np.std(np.subtract(pred_time_series[i][:len(train)], train['Close']))

        if std_sim < std:
            best = i
    # print(forecast_horizon, pred_time_series, best)
    return forecast_horizon, pred_time_series, best


def plot(df, forecast_horizon, d, best, ticker):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i in range(int(len(d))):
        if i != best:
            ax.plot(df.index[:len(df) - forecast_horizon], \
                d[i][:len(df) - forecast_horizon], \
                    alpha = 0.05)
    ax.plot(df.index[:len(df) - forecast_horizon], \
        d[best][:len(df) - forecast_horizon], \
            c = '#5398d9', linewidth = 5, label = 'Best Fitted')
    df['Close'].iloc[:len(df)-forecast_horizon].plot(c = '#d75b66', linewidth = 5, label = 'Actual')
    ax.set_title(f'Monte Carlo Simulation\nTicker: {ticker}')
    ax.legend(loc=0)
    ax.set_ylabel('Price')
    ax.set_xlabel('Date')
    plt.show()

    # comparing best fitted plus forecast with the actual history
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.plot(d[best], label = 'Best Fitted', c = '#edd170')
    ax.plot(df['Close'].tolist(), label= 'Actual', c = '#02231c')
    ax.axvline(len(df) - forecast_horizon, linestyle = ':', c = 'k')
    ax.text(len(df) - forecast_horizon-50, \
             max(max(df['Close']),max(d[best])),'Training', \
             horizontalalignment = 'center', \
             verticalalignment = 'center')
    ax.text(len(df) - forecast_horizon+50, \
             max(max(df['Close']),max(d[best])),'Testing', \
             horizontalalignment = 'center', \
             verticalalignment = 'center')

    ax.set_title(f'Training versus Testing\nTicker: {ticker}\n')
    ax.legend(loc=0)
    ax.set_ylabel('Price')
    ax.set_xlabel('T+Days')
    plt.show()
      


def main():

    start = '2010-01-01'
    end = '2020-01-01'
    ticker = 'GME'
    df = yf.download(ticker, start=start, end=end)
    df.index = pd.to_datetime(df.index)
    forecast_horizon, d, best = monte_carlo(df, 0.2, 10)
    plot(df, forecast_horizon, d, best, ticker)

if __name__ == '__main__':
    main()