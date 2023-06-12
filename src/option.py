"""
File containing the definition of the abstract class Option and the subclasses
"""
from abc import ABC, abstractmethod
from datetime import date
from asset import Asset


class Option(ABC):

    def __load__(self, ticker: str):
        """
        Method for loading the financial information of an asset from database
        :param ticker: The ticker symbol as a str object
        :return: TODO: Define return values
        """
        pass

    def update(self):
        """
        Method for retrieving updated data for the asset
        :return: Void
        """
        pass


class EuroCall(Option):

    def __init__(self, underlying: Asset, strike: float, expiration: date):
        """
        Object for European call option
        :param underlying: The underlying asset as an Asset object
        :param strike: The strike price as a float
        :param expiration: The expiration as a datetime date object
        """

        self._underlying_asset = underlying
        self._strike = strike
        self._expiration = expiration


