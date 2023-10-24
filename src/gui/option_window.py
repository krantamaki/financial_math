"""
Window for derivative (option) information
"""
import tkinter as tk
from tkinter import ttk
from config import *


_surface_image = None
_payoff_image = None

_surface_image_path = r"../data/default_image.png"
_payoff_image_path = r"../data/default_image.png"


class OptionWindow(tk.Frame):
    def __init__(self, parent, controller):
        global _surface_image, _payoff_image
        tk.Frame.__init__(self, parent)

        # Entry field for the ticker of the stock
        ticker_label = tk.Label(self, text="Underlying:", font=FONT_TUP)
        ticker_label.grid(row=0, column=0, padx=4)

        ticker_entry = tk.Entry(self, width=6, font=FONT_TUP)
        ticker_entry.grid(row=0, column=1, pady=4)
        ticker_entry.insert(0, "'ticker'")

        # Button for searching the given entry
        search_button = tk.Button(self, text="Search", font=FONT_TUP)
        search_button.grid(row=0, column=2)

        # OptionMenu for choosing the position in the option
        position_label = tk.Label(self, text="Option position:", font=FONT_TUP)
        position_label.grid(row=1, column=0, columnspan=2, padx=4)

        position_text = tk.StringVar()
        position_text.set("Select position")

        position_menu = tk.OptionMenu(self, position_text, "Long", "Short")
        position_menu.grid(row=1, column=2)
        position_menu.config(width=12)

        # OptionMenu for choosing the style of the option
        style_label = tk.Label(self, text="Option style:", font=FONT_TUP)
        style_label.grid(row=2, column=0, columnspan=2, padx=4)

        style_text = tk.StringVar()
        style_text.set("Select style")

        style_menu = tk.OptionMenu(self, style_text, "European", "American")
        style_menu.grid(row=2, column=2)
        style_menu.config(width=12)

        # OptionMenu for choosing the style of the option
        type_label = tk.Label(self, text="Option type:", font=FONT_TUP)
        type_label.grid(row=3, column=0, columnspan=2, padx=4)

        type_text = tk.StringVar()
        type_text.set("Select type")

        type_menu = tk.OptionMenu(self, type_text, "Call", "Put")
        type_menu.grid(row=3, column=2)
        type_menu.config(width=12)

        # Entry for the days till expiration of the option
        dur_label = tk.Label(self, text="Days until expiration", font=FONT_TUP)
        dur_label.grid(row=4, column=0, columnspan=2, padx=4)

        dur_entry = tk.Entry(self, width=6)
        dur_entry.grid(row=4, column=2)

        # Entry for the strike price
        strike_label = tk.Label(self, text="Strike price", font=FONT_TUP)
        strike_label.grid(row=5, column=0, columnspan=2, padx=4)

        strike_entry = tk.Entry(self, width=6)
        strike_entry.grid(row=5, column=2)

        # Entry for the current share price
        cur_label = tk.Label(self, text="Current share price", font=FONT_TUP)
        cur_label.grid(row=6, column=0, columnspan=2, padx=4)

        cur_entry = tk.Entry(self, width=6)
        cur_entry.grid(row=6, column=2)

        # Set up entries for the number of points in the finite difference mesh
        fdm_label = tk.Label(self, text="Specify the size of the FD mesh.\nThere will be nT computation\nwith nS sized linear systems",
                             font=FONT_TUP)
        fdm_label.grid(row=7, column=0, columnspan=3, rowspan=3, pady=10)

        ns_label = tk.Label(self, text="Points in S dimension (nS)", font=FONT_TUP)
        ns_label.grid(row=10, column=0, columnspan=2, padx=4)

        ns_entry = tk.Entry(self, width=6)
        ns_entry.grid(row=10, column=2)

        nt_label = tk.Label(self, text="Points in t dimension (nT)", font=FONT_TUP)
        nt_label.grid(row=11, column=0, columnspan=2, padx=4)

        nt_entry = tk.Entry(self, width=6)
        nt_entry.grid(row=11, column=2)

        # Plot the option value surface
        _surface_image = tk.PhotoImage(master=controller, file=_surface_image_path).subsample(1, 2)
        surface_image_label = tk.Label(self, image=_surface_image)
        surface_image_label.grid(row=0, column=3, rowspan=5, columnspan=4)

        # Plot the payoff function
        _payoff_image = tk.PhotoImage(master=controller, file=_payoff_image_path).subsample(1, 2)
        payoff_image_label = tk.Label(self, image=_payoff_image)
        payoff_image_label.grid(row=5, column=3, rowspan=3, columnspan=4)

        # Write the theta
        theta_value = tk.StringVar()
        theta_value.set("-")

        theta_label = tk.Label(self, text=f"Theta", font=FONT_TUP)
        theta_label.grid(row=8, column=3)

        theta_value_label = tk.Label(self, textvariable=theta_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        theta_value_label.grid(row=8, column=4)

        # Write the gamma
        gamma_value = tk.StringVar()
        gamma_value.set("-")

        gamma_label = tk.Label(self, text=f"Gamma", font=FONT_TUP)
        gamma_label.grid(row=9, column=3)

        gamma_value_label = tk.Label(self, textvariable=gamma_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        gamma_value_label.grid(row=9, column=4)

        # Write the delta
        delta_value = tk.StringVar()
        delta_value.set("-")

        delta_label = tk.Label(self, text=f"Delta", font=FONT_TUP)
        delta_label.grid(row=10, column=3)

        delta_value_label = tk.Label(self, textvariable=delta_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        delta_value_label.grid(row=10, column=4)

        # Write the value of the option
        val_value = tk.StringVar()
        val_value.set("-")

        val_label = tk.Label(self, text=f"Value", font=FONT_TUP)
        val_label.grid(row=8, column=5)

        val_value_label = tk.Label(self, textvariable=val_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        val_value_label.grid(row=8, column=6)

        # Write the probability for being in the money
        p_value = tk.StringVar()
        p_value.set("-")

        p_label = tk.Label(self, text=f"Prob. in the money", font=FONT_TUP)
        p_label.grid(row=9, column=5)

        p_value_label = tk.Label(self, textvariable=p_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        p_value_label.grid(row=9, column=6)

        # Write the risk free rate
        rf_value = tk.StringVar()
        rf_value.set("-")

        rf_label = tk.Label(self, text=f"Risk-free rate", font=FONT_TUP)
        rf_label.grid(row=10, column=5)

        rf_value_label = tk.Label(self, textvariable=rf_value, relief=tk.SUNKEN, width=5, font=FONT_TUP)
        rf_value_label.grid(row=10, column=6)


