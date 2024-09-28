import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Downloading data from S&P
data = yf.download('^GSPC', start='2010-01-01', end='2023-01-01')

data['Returns'] = data['Adj Close'].pct_change().dropna()

fig, axs = plt.subplots(2, 3, figsize=(10,10))

axs[0][0].plot(data.index, data['Returns'])
axs[0][0].set_title('Daily Returns')
axs[0][0].set_ylabel('Returns')
axs[0][0].grid(True)

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

# plot 5-day volatility forecast
axs[0][1].plot(range(1, 6), forecasted_variance.values, marker='o', label='Forecasted Variance')
axs[0][1].set_title('5-Day Volatility Forecast')
axs[0][1].set_xlabel('Forecast Horizon (Days)')
axs[0][1].set_ylabel('Forecasted Variance')
axs[0][1].grid(True)

# in-sample conditional volatiltiy to see how well the garch model captures volatility clustering

data['Volatility'] = garch_result.conditional_volatility

# plotting

# plot conditional volatility
axs[1][0].plot(data.index, data['Volatility'], label='Conditional Volatility')
axs[1][0].set_title('S&P 500 Conditional Volatility (In-sample)')
axs[1][0].set_xlabel('Date')
axs[1][0].set_ylabel('Volatility')
axs[1][0].grid(True)

# plt.show()

# plotting residuals

residuals = garch_result.resid

# print(residuals)
axs[1][1].plot(residuals)
axs[1][1].set_title('Residuals of the GARCH Model')
axs[1][1].grid(True)

# plt.show()

# using histogram to check if residuals are normally distributed 

axs[0][2].hist(residuals, bins=50, alpha=0.75, color='blue')
axs[0][2].set_title('Residuals Disitribution')
axs[0][2].grid(True)

# plt.show()

import scipy.stats as stats

stats.probplot(residuals, dist='norm', plot=plt)
plt.title('QQ Plot of Residuals')
plt.grid(True)
plt.show()

# trying out different GARCH specifications

# egarch model - captures asymmetries in volatility