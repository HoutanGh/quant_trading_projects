import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from arch import arch_model
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
import scipy.stats as stats
from arch.univariate import ARX

data = yf.download('^GSPC', start='2010-01-01', end='2023-01-01')


data['Returns'] = data['Adj Close'].pct_change() # removed pd.to_numeric because of pct_change()
data.dropna(inplace=True)
# to prevent convergence issues
data['Returns'] = data['Returns'] * 100

# print(data)

# optimal lags using information criteria

best_aic = np.inf
best_order = None

for p in range(1, 5):
    for q in range(1, 5):
        try:
            am = arch_model(data['Returns'], p=p, q=q)
            res = am.fit(disp='off')

            if res.aic < best_aic:
                best_aic = res.aic
                best_order = (p, q)
        
        except:
            continue

print(best_order)    
# p = 2, q = 2 seems the best option changes from 1, 2 after rescaling
# AIC favours models that better capture the variance in the reutrns at the new scale so 2, 2


garch_model = arch_model(data['Returns'], p=best_order[0], q=best_order[1])
garch_result = garch_model.fit(disp='off')

# checking for autocorrelation in residuals

lb_resid = acorr_ljungbox(garch_result.resid, lags=[10], return_df=True)
lb_squared = acorr_ljungbox(garch_result.resid ** 2, lags=[10], return_df=True)

print("Ljung-Box Test on Residuals:\n", lb_resid)
print("Ljung-Box Test on Squared Residuals:\n", lb_squared)

residuals = garch_result.resid

fig, axs = plt.subplots(3, 3, figsize=(15, 15))

# daily returns
axs[0, 0].plot(data.index, data['Returns'])
axs[0, 0].set_title('Daily Returns')
axs[0, 0].grid(True)

# conditional volatility
data['Volatility'] = garch_result.conditional_volatility
axs[1, 0].plot(data.index, data['Volatility'])
axs[1, 0].set_title('Conditional Volatility')
axs[1, 0].grid(True)

# residuals
axs[1, 1].plot(residuals)
axs[1, 1].set_title('Residuals of GARCH Model')
axs[1, 1].grid(True)

# histogram of Residuals
axs[0, 1].hist(residuals, bins=50, alpha=0.75, color='blue')
axs[0, 1].set_title('Residuals Distribution')
axs[0, 1].grid(True)

# QQ Plot
stats.probplot(residuals, dist='norm', plot=axs[0, 2])
axs[0, 2].set_title('QQ Plot of Residuals')

# ACF Plot
plot_acf(residuals, lags=30, ax=axs[1, 2])
axs[1, 2].set_title('ACF of Residuals')
# plt.tight_layout()
# plt.show()

# simulating

sim_data = garch_model.simulate(params=garch_result.params, nobs=5, repetitions=1000)
sim_data.head()
# simulated_returns = sim_data['data']
# axs[2, 0].plot(simulated_returns.T, alpha=0.01, color='blue')
# axs[2, 0].set_title('Simulated Returns for 5 Days')

plt.tight_layout()
plt.show()
# # backtesting parameters

# test_size = 200
# train_size = len(data) - test_size

# forecasted_volatility = []
# realised_volatility = []

# # rolling forecasts

# for i in range(train_size, len(data)):
#     train_data = data['Returns'].iloc[:i]

#     garch_model = arch_model(train_data, p=best_order[0], q=best_order[1])
#     garch_result = garch_model.fit(disp='off')

#     # forecast volatility for the next period

#     forecast = garch_result.forecast(horizon=1)
#     f_vol = np.sqrt(forecast.variance.values[-1, 0])
#     forecasted_volatility.append(f_vol)

#     # realised volatility
#     r_vol = np.abs(data['Returns'].iloc[:i])
#     realised_volatility.append(r_vol)

# # plotting the forecasted vs. realized volatility
 
# fig, ax = plt.subplots(figsize=(10, 5))
# ax.plot(forecasted_volatility, label='Forecasted Volatility')
# ax.plot(realised_volatility, label='Realised Volatility')
# ax.set_title('Rolling Forecast vs. Realised Volatility')
# ax.set_xlabel('Date')
# ax.set_ylabel('Volatility')
# ax.legend()
# ax.grid(True)
# plt.tight_layout()
# plt.show()
