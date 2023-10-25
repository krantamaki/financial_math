"""
Collection of functions used for computing basic statistics etc.
Most of these could be replaced with generic math libraries, but are
implemented here for clarity
"""
import numpy as np


def mean(data):
    """
    Computes the (arithmetic) mean for an array of data
    :param data: array_like. The data from which mean is computed
    :return: The (arithmetic) mean as a float
    """
    n = len(data)
    assert n > 0, "There has to be at least one element to compute the mean!"

    ret = sum(data) / n

    return float(ret)


def sd(data, m=None):
    """
    Computes the (sample) standard deviation for an array of data
    :param data: array_like. The data from which standard deviation is computed
    :param m: float. The mean of the data if already computed
    :return: The (sample) standard deviation as a float
    """
    n = len(data)
    assert n > 1, "There has to be at least two elements to compute the (sample) standard deviation!"

    if m is not None:
        m = mean(data)

    ret = (sum([(x_i - m)**2 for x_i in data]) / (n - 1)) ** 0.5

    return float(ret)


def cov(data_a, data_b, mean_a=None, mean_b=None):
    """
    Computes the (sample) covariance for two arrays of data
    :param data_a: array_like. One of the arrays used
    :param data_b: array_like. The secondary array
    :param mean_a: float. The mean of the array a if already computed
    :param mean_b: float. The mean of the array b if already computed
    :return: The (sample) covariance as a float
    """
    n_a = len(data_a)
    n_b = len(data_b)

    assert n_a == n_b, "The lengths of the arrays must match!"
    assert n_a > 1, "There has to be at least two elements to compute the (sample) covariance"

    N = n_a

    if mean_a is not None:
        mean_a = mean(data_a)
    if mean_b is not None:
        mean_b = mean(data_b)

    ret = sum([(data_a[i] - mean_a) * (data_b[i] - mean_b) for i in range(N)]) / (N - 1)

    return ret


def moving_average(data, lag):
    """
    Computes the moving average for the given data
    :param data: array_like. The data for which moving average is computed
    :param lag: float. The lag of the moving average
    :return: np.array
    """
    npdata = np.array(data)
    ret = []

    for i in range(len(npdata) - lag):
        ret.append(mean(npdata[i:i + lag]))

    return np.array(ret)

