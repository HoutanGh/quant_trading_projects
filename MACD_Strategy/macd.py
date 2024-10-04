import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# calculating the moving averages
def macd(signals):

    signals['ma1'] = signals['Adj Close'].rolling(window=ma1, min_periods=1, center=False).mean()
    signals['ma1'] = signals['Adj Close'].rolling(window=ma2, min_periods=1, center=False).mean()

    return signals

# signal generation


