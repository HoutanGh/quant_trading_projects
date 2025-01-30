import pandas as pd
import numpy as np
import os

class Data_Manager:
    # cleaning of financial data

    def __init__(self, data_path: str = None):
        self.data_path = data_path 

    def load_csv(self, filename, date_col, parse_dates: bool = True):

        file_path = os.path.join(self.data_path, filename) if self.data_path else filename
        df = pd.read_csv(file_path, index_col=date_col, parse_dates=parse_dates)
        df.sort_index(inplace=True)
        
        # return data frame
        return df
    
    def clean_csv(self, df, fill_method):

        df = df[~df.index.duplicated(keep='first')] # not  using drop_duplicates cos financial data has a lot of duplicates

        df.fillna(method=fill_method, inplace=True)

        return df
    
    def get_closing_prices(self, df, price_col,):
        return df[price_col]
        
        