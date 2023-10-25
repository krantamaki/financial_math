"""
Configuration file containing useful constants
"""

"""
The span from which the stock data is evaluated
Needs to be valid for the yfinance API
Choices = 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
"""
PERIOD = "1y"

"""
The interval of the datapoints (NOTE! intraday data only extends 60 days)
Needs to be valid for the yfinance API
Choices = 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
"""
INTERVAL = "1d"


"""
The price value used in computations
Choices = Open, High, Low, Close
"""
PRICE = "Close"


"""
The name of the database which holds the computed values for assets and options
"""
DATABASE = "financial_math.db"


"""
The height (in pixels used in the gui windows)
"""
HEIGHT = 515


"""
The width (in pixels used in the gui windows)
"""
WIDTH = 750


"""
The font used by the tkinter app
"""
FONT_TUP = ("Verdana", 11)


"""
The size of the earnings figure (in inches) as a tuple (width, height)
"""
EARNINGS_IMAGE_SIZE = (3.35, 1.45)


"""
The size of the price figure (in inches) as a tuple (width, height)
"""
PRICE_IMAGE_SIZE = (3.35, 1.7)
