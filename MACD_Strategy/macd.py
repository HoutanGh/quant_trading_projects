import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# calculating the moving averages
def macd(signals):

    signals['ma1'] = signals['Adj Close'].rolling(window=ma1, min_periods=1, center=False).mean()
    signals['ma2'] = signals['Adj Close'].rolling(window=ma2, min_periods=1, center=False).mean()

    return signals

# signal generation
# ma1 - short moving average is calculated over a shorter time period, more sensitive to recent price changes and reacts quickly
# ma2 - long moving average, smooths the data out more 

def signal_gen(df, method):

    signals = method(df)

    # column will store the signals whether the strategy holds a long (1) or a neutral (0)
    signals['positions'] = 0

    # compares ma1 and ma2 for each row starting from index ma1
    # if ma1 is greater or equal to ma2, upward momentum so goes long and vice versa
    signals['positions'][ma1:] = np.where(signals['ma1'][ma1:]>=signals['ma2'][ma1:], 1, 0)

    # takes the difference of consecutive values in the position columns
    signals['signals'] = signals['position'].diff()

    signals['oscillator'] = signals['ma1'] - signals['ma2']

    return signals

def plot():
    pass


