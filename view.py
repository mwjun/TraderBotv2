import PySimpleGUI as sg
from controller import show_stock_chart


class StockChartAdapter:

  def __init__(self, stock_symbol, analysis_type, date=None):
    self.stock_symbol = stock_symbol
    self.analysis_type = analysis_type
    self.date = date

  def show_chart(self):
    show_stock_chart(self.stock_symbol,
                     analysis_type=self.analysis_type,
                     date=self.date)


def show_stock_chart_window():
  layout = [[
    sg.Text("TraderBot",
            font=("Arial", 24),
            justification="center",
            pad=((0, 0), (20, 0)))
  ],
            [
              sg.CalendarButton('Choose Date', target=(1, 0), key='date'),
              sg.Ok('Confirm Date', key='DConfirm')
            ],
            [
              sg.Combo(
                ["GOOG", "AAPL", "TSLA", "FNGU", "FNGD", "VOO", "TQQQ", "TGT", "AMD", "AMC", "GME", "ROKU", "GE", "SPY", "QQQ", "IWM", "IYR", "IYF", "IYH","LAD", "PANW", "SMCI", "PLTR"],
                default_value="TSLA",
                key="-DROPDOWN-")
            ],
            [
              sg.Button("Show Stock Chart", key="-CHARTBUTTON-"),
              sg.Button("Moving Average Backtest", key="-MA_BUTTON-"),
              sg.Button("Bollinger Band Bounce Backtest", key="-BB_BUTTON-")
            ]]

  window = sg.Window("TraderBot", layout, element_justification="center")

  while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
      break
    elif event == 'DConfirm':
      print(f"Selected: {values['date']}")
    else:
      stock_symbol = values["-DROPDOWN-"]
      date = values.get('date')
      if event == "-CHARTBUTTON-":
        adapter = StockChartAdapter(stock_symbol, "stock_chart", date)
      elif event == "-MA_BUTTON-":
        adapter = StockChartAdapter(stock_symbol, "moving_average_backtest",
                                    date)
      elif event == "-BB_BUTTON-":
        adapter = StockChartAdapter(stock_symbol, "bollinger_band_backtest",
                                    date)
      else:
        continue

      adapter.show_chart()

  window.close()


if __name__ == "__main__":
  show_stock_chart_window()
