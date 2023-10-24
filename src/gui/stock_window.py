"""
Window for asset (stock) information
"""
import tkinter as tk
from tkinter import scrolledtext as st
from config import *


_price_image = None
_earnings_image = None

_price_image_path = r"../data/default_image.png"
_earnings_image_path = r"../data/default_image.png"


class StockWindow(tk.Frame):
    def __init__(self, parent, controller):
        global _price_image, _earnings_image
        tk.Frame.__init__(self, parent)

        # Entry field for the ticker of the stock
        ticker_label = tk.Label(self, text="Ticker:", font=FONT_TUP)
        ticker_label.grid(row=0, column=0)

        ticker_entry = tk.Entry(self, width=6, font=FONT_TUP)
        ticker_entry.grid(row=0, column=1, pady=4)
        ticker_entry.insert(0, "'ticker'")

        # Button for searching the given entry
        search_button = tk.Button(self, text="Search", font=FONT_TUP)
        search_button.grid(row=0, column=2)

        # Entry for the start and end date of the span shown in figure
        cal_label = tk.Label(self, text="Date range for the figure. Format dd:mm:yyyy", font=FONT_TUP)
        cal_label.grid(row=1, column=0, columnspan=3)

        cal_start = tk.Entry(self, width=12, font=FONT_TUP)
        cal_start.grid(row=2, column=0, pady=4, padx=4)
        cal_start.insert(0, "'dd:mm:yyyy'")

        dash_label = tk.Label(self, text="-", width=2, font=FONT_TUP)
        dash_label.grid(row=2, column=1)

        cal_end = tk.Entry(self, width=12, font=FONT_TUP)
        cal_end.grid(row=2, column=2, pady=4, padx=4)
        cal_end.insert(0, "'dd:mm:yyyy'")

        # Radiobutton for choosing between normal and log normal scales
        radio_label = tk.Label(self, text="Figure scaling:", font=FONT_TUP)
        radio_label.grid(row=3, column=0)

        scale = tk.IntVar(value=0)

        log_radio_button = tk.Radiobutton(self, text="Normal", variable=scale, value=0, font=FONT_TUP)
        log_radio_button.grid(row=3, column=1)

        norm_radio_button = tk.Radiobutton(self, text="Logarithmic", variable=scale, value=1, font=FONT_TUP)
        norm_radio_button.grid(row=3, column=2)

        # Entry for the moving average
        ma_label = tk.Label(self, text="Moving Average:", font=FONT_TUP)
        ma_label.grid(row=4, column=0, columnspan=2)

        ma_entry = tk.Entry(self, width=5, font=FONT_TUP)
        ma_entry.grid(row=4, column=2, pady=4, padx=4)

        # Button for updating the figure
        update_label = tk.Label(self, text="Update the figure:", font=FONT_TUP)
        update_label.grid(row=5, column=0, columnspan=2, pady=15)

        update_button = tk.Button(self, text="Update", font=FONT_TUP)
        update_button.grid(row=5, column=2, pady=15)

        # Write the drift
        drift_value = tk.StringVar()
        drift_value.set("-")

        drift_label = tk.Label(self, text=f"Drift (period={PERIOD})", font=FONT_TUP)
        drift_label.grid(row=6, column=0, columnspan=2)

        drift_value_label = tk.Label(self, textvariable=drift_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        drift_value_label.grid(row=6, column=2)

        # Write the volatility
        vol_value = tk.StringVar()
        vol_value.set("-")

        vol_label = tk.Label(self, text=f"Volatility (period={PERIOD})", font=FONT_TUP)
        vol_label.grid(row=7, column=0, columnspan=2)

        vol_value_label = tk.Label(self, textvariable=vol_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        vol_value_label.grid(row=7, column=2)

        # Description
        description_text = tk.StringVar()
        description_text.set("-")

        description_area = st.ScrolledText(self, relief=tk.SUNKEN, width=35, height=5, font=FONT_TUP, state="disabled")
        description_area.grid(row=8, column=0, columnspan=3, rowspan=4, pady=10)

        # Plot of the price
        _price_image = tk.PhotoImage(master=controller, file=_price_image_path).subsample(1, 2)
        price_image_label = tk.Label(self, image=_price_image)
        price_image_label.grid(row=0, column=3, rowspan=5, columnspan=4)

        # Plot the earnings
        _earnings_image = tk.PhotoImage(master=controller, file=_earnings_image_path).subsample(1, 2)
        earnings_image_label = tk.Label(self, image=_earnings_image)
        earnings_image_label.grid(row=5, column=3, rowspan=3, columnspan=4)

        # Write the beta
        beta_value = tk.StringVar()
        beta_value.set("-")

        beta_label = tk.Label(self, text=f"Beta", font=FONT_TUP)
        beta_label.grid(row=8, column=3)

        beta_value_label = tk.Label(self, textvariable=beta_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        beta_value_label.grid(row=8, column=4)

        # Write the present value computed from cash flows
        fcf_value = tk.StringVar()
        fcf_value.set("-")

        fcf_label = tk.Label(self, text=f"PV(FCF)", font=FONT_TUP)
        fcf_label.grid(row=9, column=3)

        fcf_value_label = tk.Label(self, textvariable=fcf_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        fcf_value_label.grid(row=9, column=4)

        # Write the dividend
        div_value = tk.StringVar()
        div_value.set("-")

        div_label = tk.Label(self, text=f"Dividend", font=FONT_TUP)
        div_label.grid(row=10, column=3)

        div_value_label = tk.Label(self, textvariable=div_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        div_value_label.grid(row=10, column=4)

        # Write the dividend yield
        div_yield_value = tk.StringVar()
        div_yield_value.set("-")

        div_yield_label = tk.Label(self, text=f"Div. Yield", font=FONT_TUP)
        div_yield_label.grid(row=11, column=3)

        div_yield_value_label = tk.Label(self, textvariable=div_yield_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        div_yield_value_label.grid(row=11, column=4)

        # Write the P/E
        pe_value = tk.StringVar()
        pe_value.set("-")

        pe_label = tk.Label(self, text=f"P/E", font=FONT_TUP)
        pe_label.grid(row=8, column=5)

        pe_value_label = tk.Label(self, textvariable=pe_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        pe_value_label.grid(row=8, column=6)

        # Write the D/E
        de_value = tk.StringVar()
        de_value.set("-")

        de_label = tk.Label(self, text=f"D/E", font=FONT_TUP)
        de_label.grid(row=9, column=5)

        de_value_label = tk.Label(self, textvariable=de_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        de_value_label.grid(row=9, column=6)

        # Write the EPS
        eps_value = tk.StringVar()
        eps_value.set("-")

        eps_label = tk.Label(self, text=f"EPS", font=FONT_TUP)
        eps_label.grid(row=10, column=5)

        eps_value_label = tk.Label(self, textvariable=eps_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        eps_value_label.grid(row=10, column=6)

        # Write the market cap
        mc_value = tk.StringVar()
        mc_value.set("-")

        mc_label = tk.Label(self, text=f"Market Cap", font=FONT_TUP)
        mc_label.grid(row=11, column=5)

        mc_value_label = tk.Label(self, textvariable=mc_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        mc_value_label.grid(row=11, column=6)


