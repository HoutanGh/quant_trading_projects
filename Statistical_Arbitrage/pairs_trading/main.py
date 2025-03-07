import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

tickers =['GME', 'AMC']
data = yf.download(tickers, period="2y")

print(data.tail())