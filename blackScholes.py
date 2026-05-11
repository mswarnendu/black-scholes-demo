import math
import yfinance as yf
from datetime import datetime, timedelta
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Basic formula, allows computation


def black_scholes_call(S, K, r, t, sigma):

    d_1 = (np.log(S/K) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
    d_2 = d_1 - sigma * math.sqrt(t)

    N_d1 = norm.cdf(d_1)
    N_d2 = norm.cdf(d_2)

    C = S * N_d1 - K * math.exp(-r * t) * N_d2  # Actual formula

    return C, d_1


def main():

    # Data download

    TICKER = input("Enter a ticker (e.g. AAPL): ")

    ticker = yf.Ticker(TICKER)

    END_DATE = datetime.today()
    START_DATE = END_DATE - timedelta(days=1825)

    data = yf.download(TICKER, start=START_DATE.strftime("%Y-%m-%d"),
                       end=END_DATE.strftime("%Y-%m-%d"))

    prices = data["Close"]

    S = prices.dropna().iloc[-1].item()  # Current prices

    rt = np.log(prices / prices.shift(1)).dropna()

    annual_vol = rt.std().item() * math.sqrt(252)  # Annualized volatility

    r = 0.04  # Assumed risk free rate

    expiration = ticker.options

    expiry = expiration[1]
    chain = ticker.option_chain(expiry)
    calls = chain.calls

    contract = calls.iloc[0]
    K = float(contract["strike"])  # Strike Price

    today = datetime.today()
    expiry_date = datetime.strptime(expiry, '%Y-%m-%d')

    DAYS_TO_EXPIRY = (expiry_date - today).days

    t = max(DAYS_TO_EXPIRY / 365, 1e-6)  # Time to expiration

    S_min = 0.5 * K
    S_max = 1.5 * K

    S_values = np.linspace(S_min, S_max, 100)
    C_values = []
    delta_values = []

    for s in S_values:

        C, d_1 = black_scholes_call(s, K, r, t, annual_vol)

        C_values.append(C)
        delta_values.append(norm.cdf(d_1))

    plt.figure(figsize=(10, 6))

    plt.plot(S_values, C_values)
    plt.title("Call Price vs Stock Price")
    plt.xlabel("Stock Price (S)")
    plt.ylabel("Call Price (C)")
    plt.axvline(K, linestyle="--", label="Strike Price")
    plt.grid(True)

    plt.figure(figsize=(10, 6))

    plt.plot(S_values, delta_values)
    plt.title("Delta vs Stock Price")
    plt.xlabel("Stock Price (S)")
    plt.ylabel("Delta (dC/dS)")
    plt.axvline(K, linestyle="--")
    plt.grid(True)

    plt.show()

    print(f"S Range: {S_min} to {S_max}")
    print("K:", K)
    print(f"Annual Volatility: {annual_vol:.6f}")
    print("S/K ratios:", S_min/K, S_max/K)


if __name__ == "__main__":
    main()
