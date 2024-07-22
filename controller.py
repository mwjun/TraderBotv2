import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from model import StockData

# Dictionary to store registered functions and their calling strings
METHOD = {}


def register(name):
  """Decorator to register passed function name and function to METHOD"""

  def decorator(fn):
    METHOD[name] = fn
    return fn

  return decorator


def execute(stock_prices, stock_dates, function):
  """Executes given function call with passed data"""
  try:
    fn = METHOD.get(function)
    if fn:
      return fn(stock_prices, stock_dates)
    else:
      print(f"Method {function} is undefined")
  except Exception as e:
    print(f"Error executing {function}: {e}")


@register("stock_chart")
def plain_chart(stock_prices, stock_dates):
  """Adds no additional data to the plot"""
  print("Plain Chart")


@register("moving_average_backtest")
def moving_average_backtest(stock_prices,
                            stock_dates,
                            short_window=30,
                            long_window=60):
  print("MAVG")
  # Convert prices and dates to python lists
  price_data = stock_prices.tolist()
  stock_dates = stock_dates.tolist()

  # Convert price data into a pandas series
  price_series = pd.Series(price_data)

  # Calculate short-term and long-term moving averages
  # Calculates signals indicating when short/long-term moving averages are above/below
  short_mavg = price_series.rolling(window=short_window, min_periods=1).mean()
  long_mavg = price_series.rolling(window=long_window, min_periods=1).mean()
  signals = np.where(short_mavg > long_mavg, -1.0, 1.0)

  # Reads buy/sell signals and executes them to zero-sum
  ctr = 0
  shares = 0
  initial_balance = 100000
  balance = initial_balance
  date = None
  prev = 0
  for price in price_series:
    date = stock_dates[ctr]
    if prev == 0:
      pass
    elif signals[ctr] < prev:
      # Buy
      print(f"buy: {price}")
      shares = balance // price
      balance = balance - (price * shares)
      print(
        f"Shares bought: {shares}\nNewBalance: {balance}\nDate: {date.strftime('%Y-%m-%d')}\n"
      )
    elif signals[ctr] > prev:
      # Sell
      print(f"Sell: {price}")
      if shares != 0:
        balance += shares * price
        print(f"Shares Sold: {shares}")
        shares = 0
      print(f"NewBalance: {balance}\nDate: {date.strftime('%Y-%m-%d')}\n")

    prev = signals[ctr]
    ctr += 1

  # If there are shares after the algorithm is run, sell remaining shares at last value
  if shares != 0:
    balance += shares * price_data[-1]
    print(
      f"Sold {shares} remaining shares at {price_data[-1]}\nNew Balance: {balance}\n"
    )
  total_returns = balance - initial_balance
  percentage_return = ((balance - initial_balance) / initial_balance) * 100

  # Plot the moving averages
  plt.plot(stock_dates, short_mavg, label="Short-term MA", color="red")
  plt.plot(stock_dates, long_mavg, label="Long-term MA", color="blue")

  # Add return text
  plt.text(
    stock_dates[-1],
    stock_prices[-1],
    f"Total Return: ${total_returns:.2f}\nPercentage Return: {percentage_return:.2f}%",
    ha="right",
    va="top",
    backgroundcolor="white")


@register("bollinger_band_backtest")
def bollinger_band_backtest(stock_prices, stock_dates):
  print("Bollinger")

  # Predefined data
  window = 20
  num_std_dev = 2
  initial_balance = 100000

  # Convert price data into a pandas series
  price_data = stock_prices.tolist()
  price_series = pd.Series(price_data)

  # Calculate rolling mean and standard deviation
  rolling_mean = price_series.rolling(window=window, min_periods=1).mean()
  rolling_std = price_series.rolling(window=window, min_periods=1).std()

  # Calculate upper and lower Bollinger Bands
  lower_band = rolling_mean - num_std_dev * rolling_std
  upper_band = rolling_mean + num_std_dev * rolling_std

  # Generate trading signals
  signals = np.zeros(len(price_data))
  signals[price_series < lower_band] = 1.0  # Buy signal
  signals[price_series > upper_band] = -1.0  # Sell signal

  # Calculate the adjusted price data (exclude last element) and signals
  price_data_adjusted = price_data[:-1]
  signals = signals[:-1]

  # Initialize variables to store cumulative returns, stock value, and balance
  cumulative_returns = np.zeros(len(price_data))
  balance = initial_balance
  shares = 0

  for i, (price, signal) in enumerate(zip(price_data_adjusted, signals)):
    current_date = stock_dates[i]

    if signal > 0:
      # Buy signal
      if balance >= price:
        tempval = balance
        tempval -= price * shares
        if tempval > 0:
          shares = shares + (balance // price)
          balance -= price * shares
          print(
            f"Buy {shares:.2f} shares at {price:.2f}, day: {current_date.strftime('%Y-%m-%d')}, balance: {balance:.2f}"
          )
        tempval = 0
      elif price > balance:
        print(
          f"Balance too low, skipped buy signal for {current_date.strftime('%Y-%m-%d')}"
        )

    elif signal < 0:
      # Sell Signal
      if shares == 0:
        print(
          f"No Shares to sell, skipping sell signal at {current_date.strftime('%Y-%m-%d')}"
        )
      else:
        balance += shares * price
        print(
          f"Sell {shares:.2f} shares at {price:.2f}, day: {current_date.strftime('%Y-%m-%d')}, balance: {balance:.2f}"
        )
        shares = 0

    cumulative_returns[i] = balance + shares * price

  if shares > 0:
    # Sell all at end
    balance = shares * price
    print(
      f"Ending, sold {shares:.2f} shares at {price:.2f}, day: {current_date.strftime('%Y-%m-%d')}, balance: {balance:.2f}"
    )

  total_returns = balance - initial_balance
  percentage_return = ((balance - initial_balance) / initial_balance) * 100

  # Plot the Bollinger Bands
  plt.plot(stock_dates,
           upper_band,
           label="Upper Bollinger Band",
           color="green",
           linestyle="--")
  plt.plot(stock_dates,
           lower_band,
           label="Lower Bollinger Band",
           color="orange",
           linestyle="--")

  plt.text(
    stock_dates[-1],
    stock_prices[-1],
    f"Total Return: ${total_returns:.2f}\nPercentage Return: {percentage_return:.2f}%",
    ha="right",
    va="bottom",
    color="black",
    backgroundcolor="white")


def show_stock_chart(stock_symbol, analysis_type="stock_chart", date=None):
  stock = StockData(stock_symbol)
  if date:
    stock_dates = stock.get_frame(date).index
    stock_prices = stock.get_frame(date)["Close"].values
  else:
    stock_dates = stock.get_frame().index
    stock_prices = stock.get_frame()["Close"].values

  # Build the base plot
  plt.plot(stock_dates, stock_prices)
  plt.xlabel("Date")
  plt.ylabel("Price")
  plt.title(f"Stock Activity for {stock_symbol}")
  plt.grid(True)

  # Decorator to build extra plot data
  execute(stock_prices, stock_dates, analysis_type)

  # Display the legend and finally show the finished graph
  plt.legend()
  plt.show()


if __name__ == "__main__":
  # Example usage:
  show_stock_chart("AAPL", analysis_type="moving_average_backtest")
