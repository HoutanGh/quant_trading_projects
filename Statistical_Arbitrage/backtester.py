import pandas as pd
import numpy as np  

class Backtester:

    def __init__(self, capital: float = 100_000.0, transaction_cost: float = 0.0):
        
        self.capital = capital
        self.transaction_cost = transaction_cost

    def backtest(self, asset1:pd.Series, asset2:pd.Series, signals: pd.Series, hedge_ratio: float):
        
        