import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Downloading data from S&P
data = yf.download('^GSPC', start='2010-01-01', end='2023-01-01')

data['Returns'] = data['Adj Close'].pct_change().dropna()

fig, axs = plt.subplots(3, 3, figsize=(10,10))

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
from arch import univariate


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
# plt.show()
# Plot autocorrelation of residuals (ACF)


from statsmodels.graphics.tsaplots import plot_acf

# axs[1][2] = plot_acf(residuals, lags=30)
# plt.title('ACF of Residuals')

# trying out different GARCH specifications

# egarch model - captures asymmetries in volatility

egarch_model = arch_model(data['Returns'].dropna(), vol='EGarch', p=1, q=1)
egarch_result = egarch_model.fit(disp="off")

print(egarch_result.summary())


# simulating future returns based on monte carlo simulations

# this didn't work, so looking at how to do it manually
# simulated_paths = garch_result.simulate(params=garch_result.params, nobs=5, method='monte carlo', repetitions=1000)

omega = garch_result.params['omega']
alpha = garch_result.params['alpha[1]']
beta = garch_result.params['beta[1]']

# print(omega, alpha, beta)
# print(garch_result.params)

n_simulations = 1000
n_days = 5

# arrays to store simuations

simulated_volatility = np.zeros((n_simulations, n_days))
simulated_returns = np.zeros((n_simulations, n_days))

# starting the simulation with the last observed volatility 

last_volatility = np.sqrt(garch_result.conditional_volatility.iloc[-1])

# print(last_volatility)

# simulating paths
# sigma_t_array = []
for i in range(n_simulations):
    sigma_t = last_volatility
    
    for t in range(n_days):
        shock = np.random.normal(0, 1)

        # simulate next period's volatility
        sigma_t_sqrd = omega + alpha * (shock**2) + beta * (sigma_t**2)
        sigma_t = np.sqrt(sigma_t_sqrd)
        # print(sigma_t)
        simulated_volatility[i, t] = sigma_t

        simulated_returns[i, t] = sigma_t * shock

#         sigma_t_array.append(sigma_t)
    
# print(len(sigma_t_array))



axs[0][2].plot(simulated_returns.T, alpha=0.01, color='blue')
axs[0][2].set_title('Simulated Returns for 5 days')
axs[0][2].grid(True)
# plt.show()


# backtesting the GARCH Model with a rolling or expanding window

rolling_predictions = []
test_size = 200

for i in range(test_size):
    train_data = data['Returns'][:-(test_size-i)]
    garch_model = arch_model(train_data.dropna(), vol='Garch', p=1, q=1)
    garch_result = garch_model.fit(disp='off')
    rolling_forecast = garch_result.forecast(horizon=1)
    rolling_predictions.append(np.sqrt(rolling_forecast.variance.values[-1, :][0]))

axs[1][2].plot(range(test_size), rolling_predictions, label='Rolling Forecasted Volatility')
axs[1][2].plot(range(test_size), data['Returns'].values[-test_size:], label='Actual Returns')
axs[1][2].legend()
axs[1][2].set_title('Rolling Forecast vs Actual Returns')
axs[1][2].grid(True)

# plt.show()

from scipy.stats import norm

# Value-at-Risk for expected loss at a given confidence over 1 day

confidence_level = 0.95
z_score = norm.ppf(confidence_level)
forecasted_volatility = np.sqrt(forecasted_variance.iloc[-1])
VaR_1day = z_score * forecasted_volatility

print(f"1-Day VaR at 95% confidence: {VaR_1day}")

