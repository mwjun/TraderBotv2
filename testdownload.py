import download
import unittest
from main import *

class TestDownload(unittest.TestCase):

    def test_exists(self):
        FNGUExists = download.StockData()
        RANDDNExists = download.StockData('erererer')

        self.assertFalse(FNGUExists.GetFrame().empty)
        self.assertTrue(RANDDNExists.GetFrame().empty)

# Unit test
class TestStockChart(unittest.TestCase):

  def test_show_stock_chart(self):
    show_stock_chart("AAPL")
    self.assertTrue(plt.get_fignums())

    with self.assertRaises(yf.TickerError):
      show_stock_chart("INVALID_SYMBOL")

    with self.assertRaises(RuntimeError):
      show_stock_chart("INVALID_STOCK")

class TestStockTradingApp(unittest.TestCase):


    # If ANY of these fail, issue with data parsing == integration fail
    def test_GUI_window_opens(self):
        with patch('PySimpleGUI.Window') as mock_window:
            mock_window_instance = mock_window.return_value
            mock_window_instance.read.return_value = (None, None)
            window = show_stock_chart(layout)
            self.assertIsNotNone(window)

    def test_show_stock_chart_button(self):
        with patch('PySimpleGUI.Window') as mock_window:
            mock_window_instance = mock_window.return_value
            mock_window_instance.read.return_value = ('-CHARTBUTTON-', {'-DROPDOWN-': 'TSLA'})
            window = show_stock_chart(layout)

    def test_moving_average_backtest_button(self):
        with patch('PySimpleGUI.Window') as mock_window:
            mock_window_instance = mock_window.return_value
            mock_window_instance.read.return_value = ('-MA_BUTTON-', {'-DROPDOWN-': 'TSLA'})
            window = show_stock_chart(layout)

    def test_bollinger_band_bounce_backtest_button(self):
        with patch('PySimpleGUI.Window') as mock_window:
            mock_window_instance = mock_window.return_value
            mock_window_instance.read.return_value = ('-BB_BUTTON-', {'-DROPDOWN-': 'TSLA'})
            window = show_stock_chart(layout)


if __name__ == '__main__':
    unittest.main()