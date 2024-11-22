import yfinance as yf
import numpy as np
import pandas as pd
from Black_Scholes_Model import black_scholes, get_stock_data  # Replace with the actual function name
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# can later change and takes an input function so same accuracy model for different functions like heston
def BS_accuracy(ticker, r=0.05):
    # r is risk free interest rate

    S, sigma = get_stock_data(ticker)
    stock = yf.Ticker(ticker)
    expiration_dates = stock.options
    
    results = []
    current_date = pd.Timestamp.today()
    # print(current_date)

    for date in expiration_dates:
        option_chain = stock.option_chain(date)
        # print(option_chain)

        T = (pd.to_datetime(date) - current_date).days / 365
        if T <= 0:
            continue

        for idx, row in option_chain.calls.iterrows():
            K = row['strike']
            bid = row['bid']
            ask = row['ask']

            if bid == 0 and ask == 0:
                continue
            market_price = (bid + ask) / 2

            model = black_scholes(S, K, T, r, sigma, option_type="call")
            model_price = model[0]
            error = model_price - market_price
            percentage_error = (error / market_price) * 100 if market_price != 0 else np.nan

            results.append({
                'Option Type': 'Call',
                'Expiration Date': date,
                'Strike': K,
                'Market Price': market_price,
                'Model Price': model_price,
                'Error': error,
                'Percentage Error': percentage_error
            })

            # Process put options
        for idx, row in option_chain.puts.iterrows():
            K = row['strike']
            bid = row['bid']
            ask = row['ask']
            if bid == 0 and ask == 0:
                continue
            market_price = (bid + ask) / 2

            model = black_scholes(S, K, T, r, sigma, option_type="put")
            model_price = model[0]
            error = model_price - market_price
            percentage_error = (error / market_price) * 100 if market_price != 0 else np.nan

            results.append({
                'Option Type': 'Put',
                'Expiration Date': date,
                'Strike': K,
                'Market Price': market_price,
                'Model Price': model_price,
                'Error': error,
                'Percentage Error': percentage_error
            })

    df_results = pd.DataFrame(results)

    return df_results


if __name__ == "__main__":
    ticker = "AAPL"
    risk_free_rate = 0.05

    df_accuracy = BS_accuracy(ticker, risk_free_rate)

    print(df_accuracy)
    
    # Fetch historical stock price data over the past year
    hist_data = yf.Ticker(ticker).history(period="1y").reset_index()

    # Create a figure with two subplots
    fig, axs = plt.subplots(2, 1, figsize=(12, 10))

    # Plot percentage errors vs strike price
    for option_type in ['Call', 'Put']:
        subset = df_accuracy[df_accuracy['Option Type'] == option_type]
        axs[0].scatter(subset['Strike'], subset['Percentage Error'], label=f'{option_type} Options')

    axs[0].axhline(0, color='black', linestyle='--')
    axs[0].set_xlabel('Strike Price')
    axs[0].set_ylabel('Percentage Error (%)')
    axs[0].set_title(f'Black-Scholes Model Pricing Errors for {ticker} Options')
    axs[0].legend()

    # Plot stock price over time
    axs[1].plot(hist_data['Date'], hist_data['Close'])
    axs[1].set_xlabel('Date')
    axs[1].set_ylabel('Stock Price')
    axs[1].set_title(f'{ticker} Stock Price Over the Past Year')

    plt.tight_layout()
    plt.show()

