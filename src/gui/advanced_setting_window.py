"""
Window for advanced settings
"""
import tkinter as tk


class AdvancedSettingsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Settings")
        label.grid(row=0, column=0)
