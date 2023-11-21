"""
File containing the definitions of abstract class Asset and subclasses of it like class Stock
"""
from abc import ABC, abstractmethod
import yfinance as yf
import numpy as np

from config import *
from math_tools import *


class Asset(ABC):

    @staticmethod
    def __load__(ticker: str):
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

        self.__ticker = ticker
        self.yfTicker = None

        info_dict = self.__load__(ticker)

        self.__description = info_dict["description"]
        self.__price = info_dict["price"]
        self.__volatility = info_dict["volatility"]  # Standard deviation of the returns
        self.__drift = info_dict["drift"]  # Mean of the returns
        self.__market_cap = info_dict["market_cap"]
        self.__earnings = info_dict["earnings"]
        self.__revenues = info_dict["revenues"]
        self.__earnings_dates = info_dict["earnings_dates"]
        self.__currency = info_dict["currency"]
        self.__eps = info_dict["eps"]
        self.__pe = info_dict["P/E"]
        self.__de = info_dict["D/E"]
        self.__dividend = info_dict["dividend"]
        self.__dividend_yield = info_dict["dividend_yield"]
        self.__last_update = info_dict["last_update"]

    def __str__(self):
        return self.__description

    def __repr__(self):
        return self.__ticker

    def __hash__(self):
        return hash(self.__ticker)

    @staticmethod
    def __load__(ticker: str):
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
        self.yfTicker = yf.Ticker(self.__ticker)
        hist = self.yfTicker.history(period=PERIOD, interval=INTERVAL)

        if len(hist) == 0:
            raise RuntimeError("Invalid ticker symbol given!")

        self.__last_update = np.datetime64("today")

        data = hist[PRICE].to_numpy()
        returns = (data[1:] - data[:-1]) / data[:-1]

        self.__drift = mean(returns)
        self.__volatility = sd(returns, m=self.__drift)

        fast_info = self.yfTicker.fast_info
        self.__price = fast_info["lastPrice"]
        self.__market_cap = fast_info["marketCap"]
        self.__currency = fast_info["currency"]

        financials = self.yfTicker.financials
        self.__earnings = financials.loc["Net Income From Continuing And Discontinued Operation"].to_numpy()
        self.__revenues = financials.loc["Total Revenue"].to_numpy()
        self.__earnings_dates = np.array(financials.columns.to_numpy(), dtype='datetime64[Y]')
        self.__eps = financials.iloc[:, 0]["Basic EPS"]
        self.__pe = self.__price / self.__eps

        latest_balance_sheet = self.yfTicker.balance_sheet.iloc[:, 0]

        debt = latest_balance_sheet["Total Debt"]
        equity = latest_balance_sheet["Stockholders Equity"]
        self.__de = debt / equity

        # Note! Doesn't work correctly if company pays multiple rounds of dividend per year
        dividends = self.yfTicker.dividends
        if len(dividends) > 0:
            self.__dividend = dividends[0]
            self.__dividend_yield = self.__dividend / self.__price
        else:
            self.__dividend = 0
            self.__dividend_yield = 0

        self.__description = self.yfTicker.info["longBusinessSummary"]

    @property
    def volatility(self):
        return self.__volatility

    @property
    def drift(self):
        return self.__drift

    @property
    def price(self):
        return self.__price

    @property
    def description(self):
        return self.__description

    @property
    def market_cap(self):
        return self.__market_cap

    @property
    def earnings(self):
        return self.__earnings

    @property
    def revenues(self):
        return self.__revenues

    @property
    def earnings_dates(self):
        return self.__earnings_dates

    @property
    def currency(self):
        return self.__currency

    @property
    def eps(self):
        return self.__eps

    @property
    def price_to_earnings(self):
        return self.__pe

    @property
    def debt_to_equity(self):
        return self.__de

    @property
    def dividend(self):
        return self.__dividend

    @property
    def dividend_yield(self):
        return self.__dividend_yield

    @property
    def last_update(self):
        return self.__last_update

