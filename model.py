import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class StockData:
  """
  Handles loading and downloading stock data from yfinance
  """

  def __init__(self, ticker='FNGU'):
    self.ticker = ticker
    self.panData = None
    self.update()

  def update(self):
    """
    Downloads stock data from January 1st, 2020 to yesterday
    """
    yesterday = datetime.today() - timedelta(days=1)
    self.panData = yf.download(tickers=self.ticker,
                               start='2020-01-01',
                               end=yesterday,
                               progress=False)
    self.clean()
    self.save_data()

  def clean(self):
    """
    Drops the {Adj Close} column from downloaded data, as it is not necessary
    """
    self.panData.drop(columns=['Adj Close'], inplace=True)

  def save_data(self):
    """
    If {./data/} does not exist, create the directory.
    Save the current ticker's downloaded data as a JSON file in ./data
    """
    if not os.path.exists("data"):
      os.makedirs("data")
    file_path = f"./data/{self.ticker}.json"
    self.panData.to_json(file_path, date_format='iso')

  def print_table(self):
    """
    Prints the contents of the current pandas dataframe
    """
    print(self.panData)

  def get_frame(self, date=None):
    """
    Returns a copy of the loaded dataframe
    If a date is given, return a copy of the dataframe from {date} to yesterday
    """
    if date:
      selected_date = pd.to_datetime(date)
      copy = self.panData.loc[selected_date:]
    else:
      copy = self.panData.copy()
    return copy

  def get_ticker(self):
    """
    Returns the current loaded ticker symbol
    """
    return self.ticker

  def set_ticker(self, new_ticker):
    """
    Sets a new ticker symbol and calls update
    """
    self.ticker = new_ticker
    self.update()
# Interface for data update related methods
class DataUpdater(ABC):

  @abstractmethod
  def Update(self):
        pass

  @abstractmethod
  def Clean(self):
        pass

#interface for data saving related methods are here defined in the class 

# Interface for data saving related methods
class DataSaver(ABC):

  @abstractmethod
  def SaveData(self):
    pass

    # StockData class now implements the DataUpdater and DataSaver interfaces
class StockDataUpdater(DataUpdater):

  def Update(self):
      self.panData = yf.download(tickers=self.ticker,
                                 start='2020-01-01',
                                 end=self.yesterday,
                                 progress=False)
      self.Clean()

  def Clean(self):
      self.panData = self.panData.drop(columns=['Adj Close'])

class StockDataSaver(DataSaver):

  def SaveData(self):
      createdDir = os.path.exists("data")
      if not createdDir:
          os.makedirs("data")
      f = open(f"./data/{self.ticker}.json", 'w+')
      self.panData.to_json(f, date_format='iso')