# Black Scholes Demo

## Overview

This is a Python program that simulates the Black-Scholes model to price European call options using real market data. It also visualizes how option price and delta change as a function of the underlying stock price.

The goal was to connect the mathematical model to real world financial data.

## Model Used

The call option price was computed using the Black-Scholes formula:

C = S · N(d1) − K · e^(−rT) · N(d2)

Where:
- C: call price
- S: underlying stock price
- K: strike price
- r: risk free rate (assumed to be 0.04)
- t: time to expiration
- N(x): standard normal cumulative distributive function

## Requirements

Run this in the terminal in the Black-Scholes

pip install yfinance scipy pandas matplotlib numpy

