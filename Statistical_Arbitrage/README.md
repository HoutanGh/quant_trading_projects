### pair trading
- data managment
- cointegration
- signals
- backtesting framework
- execution enginer (interactive brokers when I get money)
- risk management
- monitoring and reporting

### My Model:
- data manager
    - just get first with yfinance
    - then for proper backtesting, clean excel source
    - then live data 
- cointegration
    - just between two
    - maybe Johansen test for multiple (maybe not anytime soon)
- signal
- backtester
- main.py


Notes:
I actually dont even understand it yet.
- correlation
    -short-term relation? 
- cointegration
    - long-term relationship
    - cointegrated if a linear combination of their prices is stationary (constant mean and variance over time)
- spread
- mean reversion: the spread will revert to its historical mean over time
- hedge ration: the ratio of the number of units of one asset to the number of units of the other asset

## Implementation
1. Asset Selection
2. Calculate spread
3. Determine the mean and SD
4. Set  trading rules
5. Execute Trades
6. Risk Management
