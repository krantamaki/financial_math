"""
File containing the definitions of abstract class Asset and subclasses of it like class Stock
"""
from abc import ABC, abstractmethod


class Asset(ABC):

    def __load__(self, ticker: str):
        """
        Method for loading the financial information of an asset from database
        :param ticker: The ticker symbol as a str object
        :return: (The description as a str object,
                  The price as a float,
                  The volatility as a float,
                  The drift as a float)
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

        description, price, volatility, drift = self.__load__(ticker)

        self._description = description
        self._price = price
        self._volatility = volatility
        self._drift = drift

    def __str__(self):
        return self._description

    def __repr__(self):
        return self._ticker

    def __hash__(self):
        return hash(self._ticker)

    def __load__(self, ticker: str):
        return "", -1.0, -1.0, -1.0

    def update(self):
        pass


