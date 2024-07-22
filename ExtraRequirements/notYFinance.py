import os
from datetime import datetime
import urllib.request
import json
import pandas

class RawData:
    """
    Handles raw JSON download, load, and saving
    """
    def __init__(self, ticker='AAPL', range='1mo'):
        self.ticker = ticker
        self.range = range
        self.LoadedJSON = None

        self.LoadJSON(ticker, range)
        
    def LoadJSON(self, ticker=None, range=None):
        """
        Call YahooFinance API to retrieve {ticker} data from {range} years ago,
        Loads [open, high, low, close, volume] into a JSON object, Call with no args to reload JSON
        """
        if (ticker is None) or (range is None):
            ticker = self.ticker
            range = self.range
        else: 
            self.ticker = ticker

        call = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?&interval=1d&range={range}'
        response = urllib.request.urlopen(call)

        dirtyJSON = json.loads(response.read().decode("utf-8"))

        ctr = 0
        cleanedDict = {'Open': {},'High': {}, 'Low': {}, 'Close': {}, 'Volume': {}}
        for time in dirtyJSON['chart']['result'][0]['timestamp']:
            isoTime = datetime.utcfromtimestamp(time).isoformat()
            cleanedDict['Open'][isoTime] = dirtyJSON['chart']['result'][0]['indicators']['quote'][0]['open'][ctr]
            cleanedDict['High'][isoTime] = dirtyJSON['chart']['result'][0]['indicators']['quote'][0]['high'][ctr]
            cleanedDict['Low'][isoTime] = dirtyJSON['chart']['result'][0]['indicators']['quote'][0]['low'][ctr]
            cleanedDict['Close'][isoTime] = dirtyJSON['chart']['result'][0]['indicators']['quote'][0]['close'][ctr]
            cleanedDict['Volume'][isoTime] = dirtyJSON['chart']['result'][0]['indicators']['quote'][0]['volume'][ctr]

            ctr += 1

        self.LoadedJSON = json.dumps(cleanedDict)
        self.StoreJSON()
    
    def StoreJSON(self):
        """
        Creates directory 'data' if it doesn't exist, then saves the loaded
        JSON data as {ticker}.json into the 'data' directory
        """
        createdDir = os.path.exists("data")
        if not createdDir:
            os.makedirs("data")
        with open(f"./data/{self.ticker}.json", 'w+') as f:
            #json.dump(self.LoadedJSON, f)
            f.write(self.LoadedJSON + '\n')

    def GetJSON(self):
        """ JSON Getter """
        return self.LoadedJSON
    
    def GetTicker(self):
        """ Ticker Getter """
        return self.ticker

class PandasDataframe:
    """
    Formats JSON to a pandas dataframe for compat with existing code
    """
    def __init__(self, ticker='AAPL', range='1mo'):
        self.raw = None
        self.dataframe = None

        self.raw = RawData(ticker, range)
        self.dataframe = pandas.read_json(self.raw.GetJSON(), orient='columns')
        self.dataframe.index.name = 'Date'
    
    def PrintDataframe(self):
        print(self.dataframe)

    def GetFrame(self):
        return self.dataframe

    def GetTicker(self):
        return self.raw.GetTicker()