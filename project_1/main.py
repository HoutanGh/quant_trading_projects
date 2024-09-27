import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Downloading data from S&P
data = yf.download('^GSPC', start='2010-01-01', end='2023-01-01')

data['Returns'] = data['Adj Close'].pct_change().dropna()

data['Returns'].plot(title=' Daily Returns of S&P 500')

# making sure that data is numeric
data['Returns'] = pd.to_numeric(data['Returns'], errors='coerce')
# plt.show()

print("Quant Project 1")

# checking for NaN values
print(data['Returns'].isnull().sum())
from arch import arch_model

# define a GARCH(1, 1) model on the returns
garch_model = arch_model(data['Returns'].dropna(), vol='Garch', p=1, q=1)

# fit the model
garch_result = garch_model.fit(disp='off')

# print model summary
print(garch_result.summary())

# forecast the next 5 days of volatility
forecasts = garch_result.forecast(horizon=5)

# extract the forecasted variance for the next 5 days
forecasted_variance = forecasts.variance.iloc[-1]  # getting only the last forecasted row

# create a plot
plt.figure(figsize=(10,6))
plt.plot(range(1, 6), forecasted_variance.values, marker='o')
plt.title('5-Day Volatility Forecast')
plt.xlabel('Forecast Horizon (Days)')
plt.ylabel('Forecasted Variance')
plt.xticks(ticks=range(1, 6))  # ensure correct ticks for each forecasted day
plt.show()
