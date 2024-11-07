import yfinance as yf
import numpy as np
from Black_Scholes_Model import black_scholes  # Replace with the actual function name
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import datetime, timedelta

def get_nearest_expiry(stock, target_date):
    """Finds the nearest available expiration date to the target date."""
    available_dates = stock.options
    nearest_date = min(available_dates, key=lambda x: abs(datetime.strptime(x, '%Y-%m-%d') - target_date))
    return nearest_date

def get_option_data(ticker, expiry_date):
    stock = yf.Ticker(ticker)
    options = stock.option_chain(expiry_date)
    return options.calls, options.puts

def calculate_accuracy(stock_ticker, option_type="call"):
    # Fetch stock data
    stock = yf.Ticker(stock_ticker)
    current_price = stock.history(period="1d")['Close'].iloc[-1]

    # Target expiry date is 30 days out
    target_expiry_date = datetime.today() + timedelta(days=30)
    expiry_date = get_nearest_expiry(stock, target_expiry_date)

    # Fetch options data for the nearest available expiry date
    calls, puts = get_option_data(stock_ticker, expiry_date)
    options = calls if option_type.lower() == "call" else puts

    # Accuracy comparison
    predicted_prices = []
    true_prices = []
    
    for _, option in options.iterrows():
        strike_price = option['strike']
        true_price = option.get('lastPrice')  # Use .get to avoid KeyError

        # Ensure both predicted and true prices are valid before appending
        if not np.isnan(true_price):
            T = (datetime.strptime(expiry_date, '%Y-%m-%d') - datetime.today()).days / 365
            r = 0.05  # Assumed risk-free rate
            sigma = stock.history(period="1y")['Close'].pct_change().std() * np.sqrt(252)  # Annualized volatility
            
            predicted_price = black_scholes(
                S=current_price,
                K=strike_price,
                T=T,
                r=r,
                sigma=sigma,
                option_type=option_type
            )
            
            predicted_prices.append(predicted_price)
            true_prices.append(true_price)

    # Ensure lists are of the same length
    if len(predicted_prices) == len(true_prices) and len(predicted_prices) > 0:
        # Calculate metrics
        mae = mean_absolute_error(true_prices, predicted_prices)
        rmse = np.sqrt(mean_squared_error(true_prices, predicted_prices))
        print(f"Mean Absolute Error (MAE): {mae}")
        print(f"Root Mean Squared Error (RMSE): {rmse}")
    else:
        print("No valid data points for accuracy calculation.")

# Run the test for a specific stock, for example, Apple (AAPL)
calculate_accuracy("AAPL", option_type="call")
