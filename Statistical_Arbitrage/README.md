##### Plan
Going to do pairs trading model first, going to watch the video by quantbuild. Then research about Statistical Arbitrage as my understanding isn't good enough yet.
[ ] - quantbuild video
[ ] - pairs trading model
[ ] - research on SA



### pairs trading
- data management
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
- cointegration (can just be a function tbh)
    - just between two
    - maybe Johansen test for multiple (maybe not anytime soon)
    - has real time functionality (or just through every loop of the actual model run the cointegration?)
- signal
    - buy/hold/sell signals based on the z-score
    - z-score: identifies how far the spread deviates from its mean       
- backtester
- main.py
- trade analyser: best times in the day, week, month to trade
    - maybe a way to visualise it


Notes:
I actually dont even understand it yet.
- correlation
    - short-term relation? 
- cointegration
    - long-term relationship
    - cointegrated if a linear combination of their prices is stationary (constant mean and variance over time)
- spread
- mean reversion: the spread will revert to its historical mean over time
- hedge ration: the ratio of the number of units of one asset to the number of units of the other asset

## Implementation
1. Asset Selection
- through initial cointegration
### Rest is either real-time data or backtesting
2. Calculate spread
3. Determine the mean and SD
4. Set trading rules
5. Execute Trades
6. Risk Management


#### Ideas 
- market rotation   
    - avoid trading when pairs lose their cointegration
    - use regime detection to focus on pairs that perform best in the current market condition
    - limit trades during high volatility (maybe, not what reddit guy did)
- optimise entry/exit to account for shrinking spreads and faster corrections
- data pipeline and infrastructure 

- dashboard of how strategy is performing
