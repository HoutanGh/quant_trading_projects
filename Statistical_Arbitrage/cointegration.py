import numpy as np
import pandas as pd
from statsmodel.tsa.stattools import coint
import statsmodel.api as sm

class CoinIntegrationTester:
        # finding cointegrated pairs and calcualted hedge ratios

        def __init__(self, significance: float = 0.5):
            self.signficance = significance

        def find_cointegrated_pair(self, data: pd.DataFrame):
            n = data.shape[1] # number of columns
            keys = data.columns
            coint_pairs = []

            for i in range(n):
                for j in range(i+1, n):
                    asset1 = data.iloc[:, i]
                    asset2 = data.iloc[:, j]

                    coint_t, p_value = coint(asset1, asset2)
                    if p_value < self.signficance:
                         
                        # hedge ratio via linear regression 
                        hedge_ratio = self.compute_hedge_ratio(asset1, asset2)
                        coint_pairs.append((keys[i], keys[j], p_value, hedge_ratio))

            return coint_pairs
        
        def compute_hedge_ratio(self, series_y, series_x):
            X = sm.add_constant(series_x)
            model = sm.OLS(series_y, X).fit() # OLS regression model with series_y as dependent and X as independent
            
            return model.params[series_x.name]
                        