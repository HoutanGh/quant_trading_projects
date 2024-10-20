import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import random as rd
from sklearn.model_selection import train_test_split


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
    print(forecast_horizon, pred_time_series, best)
    return forecast_horizon, pred_time_series, best





def main():

    start = '2010-01-01'
    end = '2020-01-01'
    ticker = 'GE'
    df = yf.download(ticker, start=start, end=end)
    df.index = pd.to_datetime(df.index)
    monte_carlo(df, 0.2, 10)

if __name__ == '__main__':
    main()