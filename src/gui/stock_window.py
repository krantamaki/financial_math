"""
Window for asset (stock) information
"""
import numpy as np
import tkinter as tk
from tkinter import scrolledtext as st
from tkinter import messagebox as mb
from config import *
from asset import *
from visualization import *
from math_tools import moving_average

_price_image = None
_earnings_image = None

_price_image_path = r"data/default_image.png"
_earnings_image_path = r"data/default_image.png"


_default_description = "Could not find a description for the asset"


class StockWindow(tk.Frame):

    def __init__(self, parent, controller):
        global _price_image, _earnings_image
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        # Required class specific variables
        self._stock = None

        # Entry field for the ticker of the stock
        self.ticker_label = tk.Label(self, text="Ticker:", font=FONT_TUP)
        self.ticker_label.grid(row=0, column=0)

        self.ticker_entry = tk.Entry(self, width=10, font=FONT_TUP)
        self.ticker_entry.grid(row=0, column=1, pady=4)
        self.ticker_entry.insert(0, "'ticker'")

        # Button for searching the given entry
        self.search_button = tk.Button(self, text="Search", font=FONT_TUP, command=self.get_ticker)
        self.search_button.grid(row=0, column=2)

        # Entry for the start and end date of the span shown in figure
        self.cal_label = tk.Label(self, text="Date range for the figure. Format yyyy-mm-dd", font=FONT_TUP)
        self.cal_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.cal_start = tk.Entry(self, width=12, font=FONT_TUP)
        self.cal_start.grid(row=2, column=0, pady=4, padx=4)
        self.cal_start.insert(0, "'yyyy-mm-dd'")

        self.dash_label = tk.Label(self, text=":", width=2, font=FONT_TUP)
        self.dash_label.grid(row=2, column=1)

        self.cal_end = tk.Entry(self, width=12, font=FONT_TUP)
        self.cal_end.grid(row=2, column=2, pady=4, padx=4)
        self.cal_end.insert(0, "'yyyy-mm-dd'")

        # Radiobutton for choosing between normal and log normal scales
        self.radio_label = tk.Label(self, text="Figure scaling:", font=FONT_TUP)
        self.radio_label.grid(row=3, column=0, pady=5)

        self.scale = tk.IntVar(value=0)

        self.log_radio_button = tk.Radiobutton(self, text="Normal", variable=self.scale, value=0, font=FONT_TUP)
        self.log_radio_button.grid(row=3, column=1, pady=5)

        self.norm_radio_button = tk.Radiobutton(self, text="Logarithmic", variable=self.scale, value=1, font=FONT_TUP)
        self.norm_radio_button.grid(row=3, column=2, pady=5)

        # Entry for the moving average
        self.ma_label = tk.Label(self, text="Moving Average:", font=FONT_TUP)
        self.ma_label.grid(row=4, column=0, columnspan=2)

        self.ma_entry = tk.Entry(self, width=5, font=FONT_TUP)
        self.ma_entry.grid(row=4, column=2, pady=4, padx=4)

        # Label for the change in value over specified period
        self.change_value = tk.StringVar()
        self.change_value.set("-")

        self.change_label = tk.Label(self, text="Change in value on the interval:", font=FONT_TUP)
        self.change_label.grid(row=5, column=0, columnspan=2, pady=3, padx=5)

        self.change_value_label = tk.Label(self, textvariable=self.change_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.change_value_label.grid(row=5, column=2, pady=3)

        # Button for updating the figure
        self.update_label = tk.Label(self, text="Update the figure:", font=FONT_TUP)
        self.update_label.grid(row=6, column=0, columnspan=2, pady=25)

        self.update_button = tk.Button(self, text="Update", font=FONT_TUP, command=self.update_figure)
        self.update_button.grid(row=6, column=2, pady=25)

        # Write the latest share price
        self.price_value = tk.StringVar()
        self.price_value.set("-")

        self.price_label_text = tk.StringVar()
        self.price_label_text.set("Latest share price ( - ):")

        self.price_label = tk.Label(self, textvariable=self.price_label_text, font=FONT_TUP)
        self.price_label.grid(row=7, column=0, columnspan=2, pady=3, padx=5)

        self.price_value_label = tk.Label(self, textvariable=self.price_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.price_value_label.grid(row=7, column=2, pady=3)

        # Write the drift
        self.drift_value = tk.StringVar()
        self.drift_value.set("-")

        self.drift_label = tk.Label(self, text=f"Drift (period={PERIOD}, interval={INTERVAL})", font=FONT_TUP)
        self.drift_label.grid(row=8, column=0, columnspan=2, pady=3, padx=5)

        self.drift_value_label = tk.Label(self, textvariable=self.drift_value, relief=tk.SUNKEN, width=7, font=FONT_TUP)
        self.drift_value_label.grid(row=8, column=2, pady=3)

        # Write the volatility
        self.vol_value = tk.StringVar()
        self.vol_value.set("-")

        self.vol_label = tk.Label(self, text=f"Volatility (period={PERIOD}, interval={INTERVAL})", font=FONT_TUP)
        self.vol_label.grid(row=9, column=0, columnspan=2, pady=3, padx=5)

        self.vol_value_label = tk.Label(self, textvariable=self.vol_value, relief=tk.SUNKEN, width=7, font=FONT_TUP)
        self.vol_value_label.grid(row=9, column=2, pady=3)

        # Description
        self.description_area = st.ScrolledText(self, relief=tk.SUNKEN, width=35, height=6, font=FONT_TUP, state="disabled")
        self.description_area.grid(row=10, column=0, columnspan=3, rowspan=4, pady=15)

        # Plot of the price
        self._price_image = tk.PhotoImage(master=controller, file=_price_image_path).subsample(1, 2)
        self.price_image_label = tk.Label(self, image=self._price_image)
        self.price_image_label.grid(row=0, column=3, rowspan=6, columnspan=4)

        # Plot the earnings
        self._earnings_image = tk.PhotoImage(master=controller, file=_earnings_image_path).subsample(1, 2)
        self.earnings_image_label = tk.Label(self, image=self._earnings_image)
        self.earnings_image_label.grid(row=5, column=3, rowspan=4, columnspan=4)

        # Write the beta
        self.beta_value = tk.StringVar()
        self.beta_value.set("-")

        self.beta_label = tk.Label(self, text=f"Beta", font=FONT_TUP)
        self.beta_label.grid(row=10, column=3)

        self.beta_value_label = tk.Label(self, textvariable=self.beta_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.beta_value_label.grid(row=10, column=4)

        # Write the present value computed from cash flows
        self.fcf_value = tk.StringVar()
        self.fcf_value.set("-")

        self.fcf_label = tk.Label(self, text=f"PV(FCF)", font=FONT_TUP)
        self.fcf_label.grid(row=11, column=3)

        self.fcf_value_label = tk.Label(self, textvariable=self.fcf_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.fcf_value_label.grid(row=11, column=4)

        # Write the dividend
        self.div_value = tk.StringVar()
        self.div_value.set("-")

        self.div_label = tk.Label(self, text=f"Dividend", font=FONT_TUP)
        self.div_label.grid(row=12, column=3)

        self.div_value_label = tk.Label(self, textvariable=self.div_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.div_value_label.grid(row=12, column=4)

        # Write the dividend yield
        self.div_yield_value = tk.StringVar()
        self.div_yield_value.set("-")

        self.div_yield_label = tk.Label(self, text=f"Div. Yield", font=FONT_TUP)
        self.div_yield_label.grid(row=13, column=3)

        self.div_yield_value_label = tk.Label(self, textvariable=self.div_yield_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.div_yield_value_label.grid(row=13, column=4)

        # Write the P/E
        self.pe_value = tk.StringVar()
        self.pe_value.set("-")

        self.pe_label = tk.Label(self, text=f"P/E", font=FONT_TUP)
        self.pe_label.grid(row=10, column=5)

        self.pe_value_label = tk.Label(self, textvariable=self.pe_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.pe_value_label.grid(row=10, column=6)

        # Write the D/E
        self.de_value = tk.StringVar()
        self.de_value.set("-")

        self.de_label = tk.Label(self, text=f"D/E", font=FONT_TUP)
        self.de_label.grid(row=11, column=5)

        self.de_value_label = tk.Label(self, textvariable=self.de_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.de_value_label.grid(row=11, column=6)

        # Write the EPS
        self.eps_value = tk.StringVar()
        self.eps_value.set("-")

        self.eps_label = tk.Label(self, text=f"EPS", font=FONT_TUP)
        self.eps_label.grid(row=12, column=5)

        self.eps_value_label = tk.Label(self, textvariable=self.eps_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.eps_value_label.grid(row=12, column=6)

        # Write the market cap
        self.mc_value = tk.StringVar()
        self.mc_value.set("-")

        self.mc_label = tk.Label(self, text=f"Market Cap", font=FONT_TUP)
        self.mc_label.grid(row=13, column=5)

        self.mc_value_label = tk.Label(self, textvariable=self.mc_value, relief=tk.SUNKEN, width=9, font=FONT_TUP)
        self.mc_value_label.grid(row=13, column=6)

    def get_ticker(self):
        """
        Get the user input from the ticker entry
        :return: Void
        """
        global _earnings_image_path
        ticker = self.ticker_entry.get()

        try:
            # Try to load stock data
            self._stock = Stock(ticker)
            self._stock.update()
        except Exception as e:
            # Create a popup window with the error message
            mb.showerror(title="Error", message=str(e))
            self._stock = None
        else:
            # Update drift, volatility and share price
            self.drift_value.set(f"{(self._stock.drift() * 100):.2f} %")
            self.vol_value.set(f"{(self._stock.volatility() * 100):.2f} %")

            self.price_label_text.set(f"Latest share price ({self._stock.last_update()}):")
            self.price_value.set(f"{self._stock.price():.2f}")

            # Update description text
            if self._stock.description() is not None:
                self.description_area.config(state="normal")
                self.description_area.delete('1.0', tk.END)
                self.description_area.insert(tk.INSERT, self._stock.description())
                self.description_area.config(state="disabled")
            else:
                self.description_area.config(state="normal")
                self.description_area.delete('1.0', tk.END)
                self.description_area.insert(tk.INSERT, _default_description)
                self.description_area.config(state="disabled")

            # Update other values
            self.mc_value.set(f"{self._stock.market_cap():.2e}")
            self.eps_value.set(f"{self._stock.eps():.2f}")
            self.de_value.set(f"{self._stock.debt_to_equity():.2f}")
            self.pe_value.set(f"{self._stock.price_to_earnings():.2f}")
            self.div_value.set(f"{self._stock.dividend():.2f}")
            self.div_yield_value.set(f"{(self._stock.dividend_yield() * 100):.2f} %")

            # TODO: Update beta and PV(FCF)

            # Update earnings figure
            _earnings_image_path = r"tmp/earnings.png"
            plot_earnings(self._stock.earnings(), self._stock.revenues(), self._stock.earnings_dates(), _earnings_image_path, self._stock.currency())
            self._earnings_image = tk.PhotoImage(master=self.controller, file=_earnings_image_path)
            self.earnings_image_label.configure(image=self._earnings_image)

    def update_figure(self):
        global _price_image_path

        if self._stock is None:
            mb.showerror(title="Error", message="The stock must first be specified!")
            return

        lag = self.ma_entry.get()
        start = self.cal_start.get()
        end = self.cal_end.get()
        scale = self.scale.get()

        try:
            start = np.datetime64(start, 'D')
            end = np.datetime64(end, 'D')
            assert start < end
            assert end <= np.datetime64('today')
        except Exception:
            mb.showerror(title="Error", message="Improper dates provided!")
            return

        try:
            lag = int(lag)
        except Exception:
            mb.showerror(title="Error", message="Improper moving average!")
            return

        try:
            assert self._stock is not None, "A stock must be specified first"
            hist = self._stock.yfTicker.history(start=str(start), end=str(end), interval=INTERVAL)
            data = hist[PRICE]
            prices = data.to_numpy()
            dates = np.array(data.index.to_numpy(), dtype='datetime64[D]')  # Note! Doesn't work if interval is not 1d

            ma_prices = moving_average(prices, lag)
            ma_dates = dates[lag:]

            self.change_value.set(f"{(((self._stock.price() - prices[0]) / prices[0]) * 100):.2f} %")

            _price_image_path = f"tmp/price.png"
            plot_price(prices, dates, ma_prices, ma_dates, lag, scale, _price_image_path, self._stock.currency(), self._stock.volatility())
        except Exception as e:
            # Create a popup window with the error message
            mb.showerror(title="Error", message=str(e))
        else:
            self._price_image = tk.PhotoImage(master=self.controller, file=_price_image_path)
            self.price_image_label.configure(image=self._price_image)
