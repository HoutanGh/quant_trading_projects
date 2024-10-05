import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

df = yf.download('^GSPC', start='2010-01-01', end='2023-01-01')

def macd(signals):

    signals['ma1'] = signals['Adj Close'].rolling(window=ma1, min_periods=1, center=False).mean()
    signals['ma2'] = signals['Adj Close'].rolling(window=ma2, min_periods=1, center=False).mean()

    return signals

macd(df)

