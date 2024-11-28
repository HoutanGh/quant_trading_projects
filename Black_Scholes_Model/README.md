##### These are mostly notes for myself 

- BS model calculates the fair value of an option

- Gonna do Black-Scholes Model then gonna do it with heston probability then something with Monte Carlo.

- Black-Scholes assumes that the volatility is constant which is not true.

### To know:

- Call option - right to buy at specified price 
- Put option - sell at specified price

### Black-Scholes (volatility assumption)
Trying to calculate the fair price of an option by taking into account risk and time. 

- Delta - how sensitive the option price is to the underlying asset
- Gamma - rate of change of delta w.r.t underlying assest price 
- Vega - how sensitive to volatility (same for calls and puts)
- Theta - sensitivty to time decay (how much the option loses each day as it reaches expiration) 
- Rho - sensitivty to risk free interest rate

### Accuracy test
##### Realised was kinda pointless, should do backtest on returns not accuracy.
- Percentage error by strike price
- Strike price is the fixed price at which the holder of an options contract can buy or sell.

### Backtest

### Bayesian optimisation
- objective function tells optimiser how good each parameter combination is
- BO initially testing a few random combinations of parameters

#### Information I should know 

derivative, options, futures, swa
- the closer the stock price is to the strike price, the more valuable the option becomes
- higher the time to expiration, higher the premium


## AIM:
- [x] understand the backtest more
- [x] main.py file with ticker 
- [ ] graph files
- [ ] backtest files
- [ ] model files 
- [ ] heston BS Model
