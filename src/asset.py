"""
File containing the definitions of abstract class Asset and subclasses of it like class Stock
"""
from abc import ABC, abstractmethod
import yfinance as yf
import numpy as np

from config import *
from math_tools import *


class Asset(ABC):

    def __load__(self, ticker: str):
        """
        Method for loading the financial information of an asset from database
        :param ticker: The ticker symbol as a str object
        :return: (The description as a str object,
                  The price as a float,
                  The volatility as a float,
                  The drift as a float) etc.
        """
        pass

    def update(self):
        """
        Method for retrieving updated data for the asset
        :return: Void
        """
        pass


class Stock(Asset):

    def __init__(self, ticker: str):
        """
        Object for general stock in a publicly traded company
        :param ticker: The ticker symbol of the stock as a str object
        """

        self._ticker = ticker
        self.yfTicker = None

        info_dict = self.__load__(ticker)

        self._description = info_dict["description"]
        self._price = info_dict["price"]
        self._volatility = info_dict["volatility"]  # Standard deviation of the returns
        self._drift = info_dict["drift"]  # Mean of the returns
        self._market_cap = info_dict["market_cap"]
        self._earnings = info_dict["earnings"]
        self._revenues = info_dict["revenues"]
        self._earnings_dates = info_dict["earnings_dates"]
        self._currency = info_dict["currency"]
        self._eps = info_dict["eps"]
        self._pe = info_dict["P/E"]
        self._de = info_dict["D/E"]
        self._dividend = info_dict["dividend"]
        self._dividend_yield = info_dict["dividend_yield"]
        self._last_update = info_dict["last_update"]

    def __str__(self):
        return self._description

    def __repr__(self):
        return self._ticker

    def __hash__(self):
        return hash(self._ticker)

    def __load__(self, ticker):
        return {"description": None,
                "price": None,
                "drift": None,
                "volatility": None,
                "market_cap": None,
                "earnings": None,
                "revenues": None,
                "earnings_dates": None,
                "currency": None,
                "eps": None,
                "P/E": None,
                "D/E": None,
                "dividend": None,
                "dividend_yield": None,
                "last_update": None}

    def update(self):
        self.yfTicker = yf.Ticker(self._ticker)
        hist = self.yfTicker.history(period=PERIOD, interval=INTERVAL)

        if len(hist) == 0:
            raise RuntimeError("Invalid ticker symbol given!")

        self._last_update = np.datetime64("today")

        data = hist[PRICE].to_numpy()
        returns = (data[1:] - data[:-1]) / data[:-1]

        self._drift = mean(returns)
        self._volatility = sd(returns, m=self._drift)

        fast_info = self.yfTicker.fast_info
        self._price = fast_info["lastPrice"]
        self._market_cap = fast_info["marketCap"]
        self._currency = fast_info["currency"]

        financials = self.yfTicker.financials
        self._earnings = financials.loc["Net Income From Continuing And Discontinued Operation"].to_numpy()
        self._revenues = financials.loc["Total Revenue"].to_numpy()
        self._earnings_dates = np.array(financials.columns.to_numpy(), dtype='datetime64[Y]')
        self._eps = financials.iloc[:, 0]["Basic EPS"]
        self._pe = self._price / self._eps

        latest_balance_sheet = self.yfTicker.balance_sheet.iloc[:, 0]

        debt = latest_balance_sheet["Total Debt"]
        equity = latest_balance_sheet["Stockholders Equity"]
        self._de = debt / equity

        # Note! Doesn't work correctly if company pays multiple rounds of dividend per year
        dividends = self.yfTicker.dividends
        if len(dividends) > 0:
            self._dividend = dividends[0]
            self._dividend_yield = self._dividend / self._price
        else:
            self._dividend = 0
            self._dividend_yield = 0

        self._description = self.yfTicker.info["longBusinessSummary"]

    def volatility(self):
        return self._volatility

    def drift(self):
        return self._drift

    def price(self):
        return self._price

    def description(self):
        return self._description

    def market_cap(self):
        return self._market_cap

    def earnings(self):
        return self._earnings

    def revenues(self):
        return self._revenues

    def earnings_dates(self):
        return self._earnings_dates

    def currency(self):
        return self._currency

    def eps(self):
        return self._eps

    def price_to_earnings(self):
        return self._pe

    def debt_to_equity(self):
        return self._de

    def dividend(self):
        return self._dividend

    def dividend_yield(self):
        return self._dividend_yield

    def last_update(self):
        return self._last_update

