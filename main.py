import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download('^GSPC', start='2010-01-01', end='2023-01-01')
data['Returns'] = data['Adj Close'].pct_change().dropna()

data['Returns'].plot(title=' Daily Returns of S&P 500')
plt.show()

print("Quant Project 1")