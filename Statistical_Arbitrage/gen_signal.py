import pandas as pd
import numpy as np

class MeanReversionSignalGenerator:
    
    # generates trading signals based on z-score (mean reversion) 

    def __init__(self, window: int= 20, entry_threshold: float = 2.0, exit_threshold: float = 0.5):
        
        self.window = window
        self.entry_threshold = entry_threshold
        self.exit_threshold = exit_threshold
        
    def calculate_zscore(self, spread: pd.Series):
        
        mean_rolling = spread.rolling(window=self.window).mean()
        std_rolling = spread.rolling(window=self.window).std()

        zscore = (spread - mean_rolling) / std_rolling
        return zscore
    
    def generate_signals(self, spread: pd.Series) -> pd.Series:
        
        zscore = self.calculate_zscore(spread)
        signals = []
        current_position = 0

        for i in range(len(zscore)):
            if current_position == 0:
                if zscore[i] > self.entry_threshold:
                    current_position = -1
                elif zscore[i] < -self.entry_threshold:
                    current_position = 1
            else:
                if abs(zscore[i]) < self.exit_threshold:
                    current_position = 0
            
            signals.append(current_position)

        return pd.Series(signals, index=spread.index, name='signal')
    

