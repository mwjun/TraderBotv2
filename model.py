import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class StockData:
    """
    Handles loading, storing, and retrieving stock data from JSON.
    If data is not found, it downloads from Yahoo Finance.
    """

    def __init__(self, ticker='FNGU'):
        self.ticker = ticker
        self.data_path = f"./data/{self.ticker}.json"
        self.panData = None
        self.load_data()

    def load_data(self):
        """
        Loads stock data from a JSON file if available, otherwise downloads it.
        """
        if os.path.exists(self.data_path):
            print(f"✅ Loading existing data for {self.ticker} from JSON...")
            try:
                self.panData = pd.read_json(self.data_path)
                self.clean_data()
            except Exception as e:
                print(f"❌ Error reading JSON file: {e}. Downloading new data...")
                self.update()
        else:
            print(f"❌ No stored data for {self.ticker}. Downloading from Yahoo Finance...")
            self.update()

    def update(self):
        """
        Downloads stock data from January 1st, 2020 to yesterday and saves it as JSON.
        """
        yesterday = datetime.today() - timedelta(days=1)
        self.panData = yf.download(
            tickers=self.ticker,
            start='2020-01-01',
            end=yesterday,
            progress=False,
            auto_adjust=False
        )

        if self.panData.empty:
            print(f"❌ Failed to download data for {self.ticker}. Check ticker symbol.")
            return

        print(f"📥 Downloaded Data Columns: {self.panData.columns}")  # Debugging

        # Extract only 'Close' column and flatten MultiIndex if necessary
        if isinstance(self.panData.columns, pd.MultiIndex):
            self.panData = self.panData['Close']
        else:
            self.panData = self.panData[['Close']]

        # Rename column properly to ensure consistency
        self.panData.columns = ['Close']

        self.clean_data()
        self.save_data()

    def clean_data(self):
        """
        Converts all data to numeric and ensures proper format.
        """
        print("🧹 Cleaning Data...")

        # Ensure data is numeric and drop missing values
        self.panData = self.panData.apply(pd.to_numeric, errors='coerce')
        self.panData.dropna(inplace=True)

        print("✅ Data cleaned successfully!")

    def save_data(self):
        """
        Saves the current ticker's downloaded data as a JSON file in ./data.
        """
        os.makedirs("data", exist_ok=True)
        self.panData.to_json(self.data_path, date_format='iso')
        print(f"✅ Data saved to {self.data_path}")

    def get_frame(self, date=None):
        """
        Returns a copy of the stored dataframe.
        If a date is given, returns a filtered dataframe from that date onward.
        """
        if self.panData is None or self.panData.empty:
            print(f"❌ Error: No stock data available for {self.ticker}.")
            return pd.DataFrame()

        if 'Close' not in self.panData.columns:
            print(f"❌ 'Close' column missing in data. Available columns: {self.panData.columns}")
            return pd.DataFrame()

        if date:
            selected_date = pd.to_datetime(date)
            return self.panData.loc[selected_date:]
        return self.panData.copy()

    def get_ticker(self):
        """Returns the current loaded ticker symbol"""
        return self.ticker

    def set_ticker(self, new_ticker):
        """Sets a new ticker symbol and loads data for it"""
        self.ticker = new_ticker
        self.load_data()
