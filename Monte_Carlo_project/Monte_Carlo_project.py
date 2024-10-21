import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import random as rd
from sklearn.model_selection import train_test_split

global colorlist
colorlist=['#fffb77',
 '#fffa77',
 '#fff977',
 '#fff876',
 '#fff776',
 '#fff676',
 '#fff576',
 '#fff475',
 '#fff375',
 '#fff275',
 '#fff175',
 '#fff075',
 '#ffef74',
 '#ffef74',
 '#ffee74',
 '#ffed74',
 '#ffec74',
 '#ffeb73',
 '#ffea73',
 '#ffe973',
 '#ffe873',
 '#ffe772',
 '#ffe672',
 '#ffe572',
 '#ffe472',
 '#ffe372',
 '#ffe271',
 '#ffe171',
 '#ffe071',
 '#ffdf71',
 '#ffde70',
 '#ffdd70',
 '#ffdc70',
 '#ffdb70',
 '#ffda70',
 '#ffd96f',
 '#ffd86f',
 '#ffd76f',
 '#ffd66f',
 '#ffd66f',
 '#ffd56e',
 '#ffd46e',
 '#ffd36e',
 '#ffd26e',
 '#ffd16d',
 '#ffd06d',
 '#ffcf6d',
 '#ffce6d',
 '#ffcd6d',
 '#ffcc6c',
 '#ffcb6c',
 '#ffca6c',
 '#ffc96c',
 '#ffc86b',
 '#ffc76b',
 '#ffc66b',
 '#ffc56b',
 '#ffc46b',
 '#ffc36a',
 '#ffc26a',
 '#ffc16a',
 '#ffc06a',
 '#ffbf69',
 '#ffbe69',
 '#ffbd69',
 '#ffbd69',
 '#ffbc69',
 '#ffbb68',
 '#ffba68',
 '#ffb968',
 '#ffb868',
 '#ffb768',
 '#ffb667',
 '#ffb567',
 '#ffb467',
 '#ffb367',
 '#ffb266',
 '#ffb166',
 '#ffb066',
 '#ffaf66',
 '#ffad65',
 '#ffac65',
 '#ffab65',
 '#ffa964',
 '#ffa864',
 '#ffa763',
 '#ffa663',
 '#ffa463',
 '#ffa362',
 '#ffa262',
 '#ffa062',
 '#ff9f61',
 '#ff9e61',
 '#ff9c61',
 '#ff9b60',
 '#ff9a60',
 '#ff9860',
 '#ff975f',
 '#ff965f',
 '#ff955e',
 '#ff935e',
 '#ff925e',
 '#ff915d',
 '#ff8f5d',
 '#ff8e5d',
 '#ff8d5c',
 '#ff8b5c',
 '#ff8a5c',
 '#ff895b',
 '#ff875b',
 '#ff865b',
 '#ff855a',
 '#ff845a',
 '#ff8259',
 '#ff8159',
 '#ff8059',
 '#ff7e58',
 '#ff7d58',
 '#ff7c58',
 '#ff7a57',
 '#ff7957',
 '#ff7857',
 '#ff7656',
 '#ff7556',
 '#ff7455',
 '#ff7355',
 '#ff7155',
 '#ff7054',
 '#ff6f54',
 '#ff6d54',
 '#ff6c53',
 '#ff6b53',
 '#ff6953',
 '#ff6852',
 '#ff6752',
 '#ff6552',
 '#ff6451',
 '#ff6351',
 '#ff6250',
 '#ff6050',
 '#ff5f50',
 '#ff5e4f',
 '#ff5c4f',
 '#ff5b4f',
 '#ff5a4e',
 '#ff584e',
 '#ff574e',
 '#ff564d',
 '#ff544d',
 '#ff534d',
 '#ff524c',
 '#ff514c',
 '#ff4f4b',
 '#ff4e4b',
 '#ff4d4b',
 '#ff4b4a',
 '#ff4a4a']

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
      
# checking if surge in simulations increases the prediction accuracy

def test(df, ticker, sim_start, sim_end, sim_delta):
    simulations = np.arange(sim_start, sim_end + sim_delta, sim_delta)
    table = pd.DataFrame(index = simulations, columns=['Prediction'])
    table['Prediction'] = 0

    for i in simulations:
        
        forecast_horizon, d, best = monte_carlo(df, test_size=100, simulations=i)
        
        actual_return = np.sign(df['Close'].iloc[len(df) - forecast_horizon] - df['Close'].iloc[-1])
        best_fitted_return = np.sign(d[best][len(df) - forecast_horizon] - d[best][-1])

        table.at[i, 'Prediction'] = 1 if actual_return ==  best_fitted_return else - 1

    plt.figure(figsize=(10, 5))
    colors = ['#d75b66' if x == -1 else '#5398d9' for x in table['Prediction']]
    plt.bar(table.index.astype(str), table['Prediction'], color=colors)
    plt.xlabel('Number of Simulations')
    plt.ylabel('Prediction Accuracy')
    plt.title(f"Prediction Accuracy vs. Number of Simulations\nTicker: {ticker}")
    plt.xticks(rotation=45)
    plt.yticks([-1, 1], ['Failure', 'Success'])
    plt.show()


def main():

    start = '2010-01-01'
    end = '2020-01-01'
    ticker = 'GME'
    df = yf.download(ticker, start=start, end=end)
    df.index = pd.to_datetime(df.index)
    forecast_horizon, d, best = monte_carlo(df, 0.2, 10)
    plot(df, forecast_horizon, d, best, ticker)
    sim_start = 100
    sim_end = 500
    sim_delta = 100
    test(df, ticker, sim_start, sim_end, sim_delta)

if __name__ == '__main__':
    main()