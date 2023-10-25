"""
Collection of functions for visualization
"""
from matplotlib import pyplot as plt
import numpy as np
from config import *
from math_tools import moving_average


def plot_earnings(earnings, revenues, dates, save_path, currency):
    """
    Plot the earnings and revenues as a bar plot
    :param earnings:
    :param revenues:
    :param dates:
    :param save_path:
    :param currency:
    :return: Void
    """
    assert len(earnings) == len(revenues), "The number of earnings and revenues must match!"
    assert len(earnings) == len(dates), "The number of earnings and dates must match"

    x_axis = np.arange(len(dates))

    plt.rc('font', size=7)

    fig = plt.figure()
    fig.set_size_inches(EARNINGS_IMAGE_SIZE[0], EARNINGS_IMAGE_SIZE[1])

    plt.bar(x_axis - 0.2, revenues, 0.4, label="Revenues")
    plt.bar(x_axis + 0.2, earnings, 0.4, label="Earnings")

    plt.xticks(x_axis, dates)
    plt.ylabel(f"Value ({currency})")
    plt.legend(loc='upper right')
    plt.tight_layout(pad=0.5)

    plt.savefig(save_path)
    plt.close(fig)


def plot_price(prices, dates, ma_prices, ma_dates, lag, use_log_scale, save_path, currency, volatility):
    """
    Plot the share price as a line plot
    :param prices:
    :param dates:
    :param ma_prices:
    :param ma_dates:
    :param lag:
    :param use_log_scale:
    :param save_path:
    :param currency:
    :param volatility:
    :return:
    """

    assert len(prices) == len(dates), "The number of prices should match the number of dates!"
    assert len(ma_prices) == len(ma_dates), "The number of moving average prices should match the number of dates!"
    assert lag > 0, "Moving average can't be computed with negative lag!"

    plt.rc('font', size=7)

    fig = plt.figure()
    fig.set_size_inches(PRICE_IMAGE_SIZE[0], PRICE_IMAGE_SIZE[1])

    plt.plot(dates, prices, label="Price")
    plt.fill_between(dates, (1 - volatility) * prices, (1 + volatility) * prices, alpha=0.25)

    plt.plot(ma_dates, ma_prices, alpha=0.85, linewidth=0.85, label=f"Moving average ({lag})")

    if use_log_scale:
        plt.yscale('log')

    plt.ylabel(f"Value ({currency})")
    plt.legend(loc='upper left')
    fig.autofmt_xdate()
    plt.tight_layout(pad=0.5)

    plt.savefig(save_path)
    plt.close(fig)

