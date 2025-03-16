import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from model import StockData

# Dictionary to store registered functions
METHOD = {}

def register(name):
    """Decorator to register passed function name and function to METHOD"""
    def decorator(fn):
        METHOD[name] = fn
        return fn
    return decorator

def execute(stock_prices, stock_dates, function):
    """Executes the selected backtesting function"""
    try:
        fn = METHOD.get(function)
        if fn:
            print(f"Executing function: {function}")  # Debugging
            return fn(stock_prices, stock_dates)
        else:
            print(f"Method {function} is undefined")
    except Exception as e:
        print(f"Error executing {function}: {e}")

@register("stock_chart")
def plain_chart(stock_prices, stock_dates):
    """Plots only stock prices"""
    print("Displaying Stock Chart...")  # Debugging
    plt.plot(stock_dates, stock_prices, label="Stock Prices", color="black")

@register("moving_average_backtest")
def moving_average_backtest(stock_prices, stock_dates, short_window=30, long_window=60):
    """Backtests a moving average strategy with $100,000 initial balance"""
    print("Running Moving Average Backtest...")  # Debugging

    if len(stock_prices) == 0 or len(stock_dates) == 0:
        print("Error: No stock data available for analysis.")
        return

    price_series = pd.Series(stock_prices.tolist())

    # Compute moving averages
    short_mavg = price_series.rolling(window=short_window, min_periods=1).mean()
    long_mavg = price_series.rolling(window=long_window, min_periods=1).mean()
    signals = np.where(short_mavg > long_mavg, -1.0, 1.0)

    # Trading simulation
    initial_balance = 100000
    balance = initial_balance
    shares = 0
    prev_signal = 0

    for i, price in enumerate(price_series):
        if signals[i] < prev_signal:  # Buy
            shares = balance // price
            balance -= shares * price
            print(f"BUY: {shares} shares at {price:.2f}")
        elif signals[i] > prev_signal and shares > 0:  # Sell
            balance += shares * price
            print(f"SELL: {shares} shares at {price:.2f}")
            shares = 0
        prev_signal = signals[i]

    # Final Sell if shares remain
    if shares > 0:
        balance += shares * price_series.iloc[-1]
        print(f"Final SELL: {shares} shares at {price_series.iloc[-1]:.2f}")

    # Compute returns
    total_returns = balance - initial_balance
    percentage_return = (total_returns / initial_balance) * 100

    # Plot stock and moving averages
    plt.plot(stock_dates, price_series, label="Stock Prices", color="black")
    plt.plot(stock_dates, short_mavg, label="Short-term MA", color="red", linestyle="--")
    plt.plot(stock_dates, long_mavg, label="Long-term MA", color="blue", linestyle="--")

    # Display return text
    plt.text(
        stock_dates[-1],
        price_series.iloc[-1],
        f"Total Return: ${total_returns:.2f}\n% Return: {percentage_return:.2f}%",
        ha="right",
        va="top",
        backgroundcolor="white"
    )

@register("bollinger_band_backtest")
def bollinger_band_backtest(stock_prices, stock_dates, window=20, num_std_dev=2):
    """Backtests a Bollinger Bands trading strategy with $100,000 initial balance"""
    print("Running Bollinger Band Backtest...")  # Debugging

    if len(stock_prices) == 0 or len(stock_dates) == 0:
        print("Error: No stock data available for analysis.")
        return

    price_series = pd.Series(stock_prices.tolist())

    # Compute Bollinger Bands
    rolling_mean = price_series.rolling(window=window, min_periods=1).mean()
    rolling_std = price_series.rolling(window=window, min_periods=1).std()
    upper_band = rolling_mean + num_std_dev * rolling_std
    lower_band = rolling_mean - num_std_dev * rolling_std

    # Trading simulation
    initial_balance = 100000
    balance = initial_balance
    shares = 0

    for i, price in enumerate(price_series):
        if price < lower_band.iloc[i] and balance >= price:  # Buy
            shares = balance // price
            balance -= shares * price
            print(f"BUY: {shares} shares at {price:.2f}")
        elif price > upper_band.iloc[i] and shares > 0:  # Sell
            balance += shares * price
            print(f"SELL: {shares} shares at {price:.2f}")
            shares = 0

    # Final Sell
    if shares > 0:
        balance += shares * price_series.iloc[-1]
        print(f"Final SELL: {shares} shares at {price_series.iloc[-1]:.2f}")

    # Compute returns
    total_returns = balance - initial_balance
    percentage_return = (total_returns / initial_balance) * 100

    # Plot stock price and Bollinger Bands
    plt.plot(stock_dates, price_series, label="Stock Prices", color="black")
    plt.plot(stock_dates, rolling_mean, label="Rolling Mean", color="orange")
    plt.plot(stock_dates, upper_band, label="Upper Band", color="green", linestyle="--")
    plt.plot(stock_dates, lower_band, label="Lower Band", color="red", linestyle="--")

    # Display return text
    plt.text(
        stock_dates[-1],
        price_series.iloc[-1],
        f"Total Return: ${total_returns:.2f}\n% Return: {percentage_return:.2f}%",
        ha="right",
        va="bottom",
        backgroundcolor="white"
    )

def show_stock_chart(stock_symbol, analysis_type="stock_chart", start_date=None):
    """
    Displays the stock chart with the selected backtest strategy.
    If start_date is provided, data is filtered from that date onward.
    """

    print(f"🔍 Fetching stock data for: {stock_symbol} from JSON...")
    if start_date:
        print(f"Date filter provided => {start_date}")  # Debugging

    stock = StockData(stock_symbol)

    # If a date was passed, filter from that date onward
    stock_data = stock.get_frame(start_date)

    if stock_data.empty:
        print(f"❌ Error: No data found for {stock_symbol}.")
        return

    # Extract arrays for backtesting
    stock_dates = stock_data.index
    stock_prices = stock_data["Close"].values

    print(f"📊 Loaded {len(stock_dates)} data points for {stock_symbol}.")  # Debugging
    print(f"📅 First Date: {stock_dates[0]}, Last Date: {stock_dates[-1]}")  # Debugging

    # If there's no data in the selected range
    if len(stock_dates) == 0 or len(stock_prices) == 0:
        print("❌ No data available for the selected stock or date range.")
        return

    # Clear figure before plotting new chart
    plt.figure(figsize=(12, 6))
    plt.clf()

    # Execute selected backtesting strategy
    execute(stock_prices, stock_dates, analysis_type)

    # Ensure the figure updates
    plt.legend()
    plt.draw()
    plt.pause(0.01)  # Small delay to force update
    plt.show(block=True)  # Keep the window open
