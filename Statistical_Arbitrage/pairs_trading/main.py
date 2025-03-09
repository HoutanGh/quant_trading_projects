import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

# data loading
tickers =['GME', 'AMC', 'BB', 'NOK']
data = yf.download(tickers, start='2021-01-01', end='2025-01-01', auto_adjust=False)['Adj Close']

print(data.head())

def calc_adj_close(data):
    pass


# finding cointegrating pair

def find_cointegrated_pairs(data):

    pairs = []

    n = data.shape[1]
    for i in range(n):
        for j in range(i+1, n):
            score, pvalue, _ = coint(data.iloc[:, i], data.iloc[:, j])
            # print(score, pvalue) # should just get one for each variable
            if pvalue < 0.05:
                pairs.append((data.columns[i], data.columns[j], pvalue))
        return pd.DataFrame(pairs, columns=['stock1', 'stock2', 'pvalue'])
    


def calc_spread(pairs_df):
    stock1, stock2 = pairs_df['stock1'], pairs_df['stock2']
    print(stock1, stock2)
    spread = data[stock1] - data[stock2]

    mean = spread.rolling(30).mean()
    std = spread.rolling(30).std()
    z_score = (spread - mean) / std

    
    return z_scoreS

# trading rules

def sim_trades(z_score, entry=2, exit=1):
    position = 0
    returns = []
    pass




if __name__ == "__main__":
    find_cointegrated_pairs(data)
    pairs_df = find_cointegrated_pairs(data)
    print(f"Cointegrated Pairs:\n {pairs_df}")

    spread = calc_spread(pairs_df)
    print((len(spread) / len(spread.isna())) * 100) 