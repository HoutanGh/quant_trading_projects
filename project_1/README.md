# GARCH Model for Volatility Forecasting

Financial time series often exhibit volatility clustering where if there is a period of high volatility it is followed by high volatility and vice versa. 

GARCH Model components:
- mean equation: assume that the returns are zero-mean or follow simple autoregresive process (time series model where the current value of the series is explained by its past values)
- variance equation: models the conditional volatility as a function of past squared residuals and past vavariances
- p and q parameters: p represents the number of lagged variances and q the number of lagged squared residuals (how many values they look back at)

The p and q parameters are determined by seeing the combination that minimises the Akaike Information Criterion (AIC). AIC = 2k - 2ln(L). The code goes through a loop of initialising a model comparing the AIC of the current model with the previous and if so updating the best order. 

We check for autocorrelation in the residuals
