# GARCH Model for Volatility Forecasting
### This is mostly notes for myself rather than just a textbook README.md file

Financial time series often exhibit volatility clustering where if there is a period of high volatility it is followed by high volatility and vice versa. 

GARCH Model components:
- mean equation: assume that the returns are zero-mean or follow simple autoregresive process (time series model where the current value of the series is explained by its past values)
- variance equation: models the conditional volatility as a function of past squared residuals and past vavariances
- p and q parameters: p represents the number of lagged variances and q the number of lagged squared residuals (how many values they look back at)

The p and q parameters are determined by seeing the combination that minimises the Akaike Information Criterion (AIC). AIC = 2k - 2ln(L). The code goes through a loop of initialising a model comparing the AIC of the current model with the previous and if so updating the best order. 

We check for autocorrelation (correlation of times series with its own past values)  in the residuals (difference between observed and predicted values). Use the Ljung-box Test, the equation takes in the sample size, the autocorrelation at a certain lag, summed over the number of lags being tested.

Also calculate the squared residuals to detect remaining ARCH effects (patterns of volatility). 

Simulation carried out, following the core mechanics of the GARCH model, with the assumption that the conditional variance of returns depends on previous variances and past squared returns.

For the backtesting, we carry a rolling window approach. Key concepts are:
- define a fixed window size
- use the data to compute a statistic or fit a model (in this case the GARCH model)
- move the window up by one observation
- repeat 

Also code plots all the different features calculated/taken.

QQ plot checks for normality of residuals, deviations may suggest heavy tails or skewness.

## Notes and Assumptions
- Returns are conditionally normally distributed with time-varying volatility.
- Scaling returns to improve numerical stability
- Ljung-Box test 
- QQ plot
