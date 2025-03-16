import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from controller import show_stock_chart

class StockChartAdapter:
    """
    Handles user input (symbol, date, analysis) and calls show_stock_chart().
    """

    def __init__(self, stock_symbol, analysis_type, date=None):
        self.stock_symbol = stock_symbol
        self.analysis_type = analysis_type
        self.date = date  # This will be retrieved from the Calendar if the user checks "Use Date Filter"

    def show_chart(self):
        """
        Calls show_stock_chart() with the selected parameters.
        """
        show_stock_chart(
            self.stock_symbol,
            analysis_type=self.analysis_type,
            start_date=self.date  # The chosen date (or None if not using date filter)
        )


def run_gui():
    """Launches the Tkinter-based GUI, allowing the user to pick a date from a Calendar and resize the window."""
    
    def on_submit(analysis_type):
        """Captures user’s choices (symbol, date filter) and calls show_chart()."""
        stock_symbol = stock_var.get()
        
        # If the user checked 'Use Date Filter', get the date from the Calendar
        chosen_date = None
        if date_var.get():
            # .get_date() returns a string in the specified date pattern, e.g. "2025-03-13"
            chosen_date_str = cal.get_date()
            print("DEBUG: chosen_date_str =>", chosen_date_str)
            chosen_date = chosen_date_str

        if not stock_symbol:
            messagebox.showerror("Error", "Please select a stock symbol!")
            return

        adapter = StockChartAdapter(stock_symbol, analysis_type, chosen_date)
        adapter.show_chart()

    # Create the main window
    root = tk.Tk()
    root.title("TraderBot - Calendar (Resizable)")

    # 1) (Optional) Set an initial window size, e.g. 800×600
    root.geometry("800x600")

    # 2) Allow the user to resize the window
    root.resizable(True, True)  # (width_resizable=True, height_resizable=True)

    ttk.Label(root, text="TraderBot", font=("Arial", 18)).pack(pady=10)

    # Stock Symbol Selection
    ttk.Label(root, text="Select Stock Symbol:").pack(pady=5)
    stock_var = tk.StringVar(value="GOOG")
    stock_dropdown = ttk.Combobox(
        root, textvariable=stock_var, state="readonly",
        values=[
            "GOOG", "AAPL", "TSLA", "FNGU", "FNGD", "VOO", "TQQQ",
            "TGT", "AMD", "AMC", "GME", "ROKU", "GE", "SPY", "QQQ",
            "IWM", "IYR", "IYF", "IYH", "LAD", "PANW", "SMCI", "PLTR"
        ]
    )
    stock_dropdown.current(0)
    stock_dropdown.pack(pady=5)

    # Date Selection
    ttk.Label(root, text="Select Date (Optional):").pack(pady=5)
    date_var = tk.BooleanVar(value=False)

    # A larger Calendar widget with month/year dropdown for quick selection
    cal = Calendar(
        root,
        selectmode='day',
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
        date_pattern='yyyy-mm-dd'  # or "mm/dd/yyyy" if you prefer
    )
    cal.pack(pady=10)

    # Checkbox to confirm usage of the date filter
    confirm_date_check = ttk.Checkbutton(root, text="Use Date Filter", variable=date_var)
    confirm_date_check.pack(pady=5)

    # Buttons for strategies
    ttk.Button(root, text="Show Stock Chart", command=lambda: on_submit("stock_chart")).pack(pady=5)
    ttk.Button(root, text="Moving Average Backtest", command=lambda: on_submit("moving_average_backtest")).pack(pady=5)
    ttk.Button(root, text="Bollinger Band Bounce Backtest", command=lambda: on_submit("bollinger_band_backtest")).pack(pady=5)

    # Exit button
    ttk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_gui()