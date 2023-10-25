"""
Module for tkinter interface
The multipage app is constructed following tutorial:
https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
"""
import tkinter as tk
import sys
from config import *
from gui.stock_window import *
from gui.option_window import *
from gui.advanced_setting_window import *


# Global variable for the main tkinter application
_app = None


class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)

        self.title("Financial Mathematics")

        # Create the menubar
        menubar = tk.Menu(self)

        menubar.add_command(label="Stock", command=self.show_stock_window)
        menubar.add_command(label="Option", command=self.show_option_window)
        menubar.add_command(label="Advanced settings", command=self.show_advanced_settings_window)

        self.config(menu=menubar)

        # Container for holding the Frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # The array holding the frames
        self.frames = {}

        for window_type in (StockWindow, OptionWindow, AdvancedSettingsWindow):
            frame = window_type(container, self)
            self.frames[window_type] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Initially show the stock page
        self.show_stock_window()

    def show_frame(self, window_type):
        frame = self.frames[window_type]
        frame.tkraise()

    def show_stock_window(self):
        self.show_frame(StockWindow)

    def show_option_window(self):
        self.show_frame(OptionWindow)

    def show_advanced_settings_window(self):
        self.show_frame(AdvancedSettingsWindow)


def start():
    global _app
    _app = TkinterApp()

    _app.mainloop()

