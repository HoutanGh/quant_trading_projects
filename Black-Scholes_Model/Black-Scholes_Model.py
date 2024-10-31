import numpy as np
from scipy.stats import norm
import yfinance as yf 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # common factors for Greeks calculations 
    N_d1 = norm.cdf(d1)
    N_neg_d1 = norm.cdf(-d1)
    pdf_d1 = norm.pdf(d1)

    # calculate option price based on type and Greeks
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = N_d1
        theta = - (S * pdf_d1 * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = N_neg_d1 - 1
        theta = - (S * pdf_d1 * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    gamma = pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * pdf_d1 * np.sqrt(T)
    
    
    return price, {
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega / 100,  # Scaled for 1% change in volatility
        "Theta": theta / 365,  # Daily Theta
        "Rho": rho / 100      # Scaled for 1% change in interest rate
    }


def get_stock_data(ticker):
    ticker = yf.Ticker(ticker)
    S = ticker.history(period="1d")['Close'][0]

    sigma = ticker.history(period="1y")['Close'].pct_change().std() * np.sqrt(252) # annualised volatility

    return S, sigma


if __name__ == "__main__":
    # Parameters for an option
    S, sigma = get_stock_data(ticker="AAPL")       # Strike price
    K = S * 1.05
    T = 1           # Time to expiration in years
    r = 0.05        # Risk-free interest rate (5%)

    call_price, call_greeks = black_scholes(S, K, T, r, sigma, option_type="call")
    put_price, put_greeks = black_scholes(S, K, T, r, sigma, option_type="put")

    # Print results
    print(f"Call Option Price: {call_price}")
    print(f"Put Option Price: {put_price}")
    
    print("\nCall Option Greeks:")
    for greek, value in call_greeks.items():
        print(f"{greek}: {value}")

    print("\nPut Option Greeks:")
    for greek, value in put_greeks.items():
        print(f"{greek}: {value}")