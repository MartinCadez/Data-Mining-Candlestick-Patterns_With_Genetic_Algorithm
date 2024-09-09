"""
Module Name: fitness_functions.py
Description: Need to update!

Last Updated: 2024-09-01
"""

from math import log as ln, sqrt
from statistics import mean


def total_return(log_returns: list[float]) -> float:
    """
    Calculate the total return from a list of log returns.

    Parameters :
    -------
        - `log_returns` : List containing log returns for each candlestick

    Returns :
    -------
        - `float` : Non-negative total return
    """
    return max(round(sum(log_returns), 2), 0)


def profit_factor(log_returns: list[float]) -> float:
    """
    Calculate the profit factor from a list of log returns.

    Parameters :
    -------
        - `log_returns` : List containing log returns for each candlestick

    Returns :
    -------
        - `float` : Non-negative profit factor

    Note :
    -------
        - If the negative returns are zero, the profit factor is calculated as the sum of positive returns divided by 0.01
    """

    # Pattern needs to be matched at least 2.5% of the time (avoiding noise)
    pattern_matches = sum(1 for r in log_returns if isinstance(r, float))
    if pattern_matches < 0.025 * len(log_returns):
        return 0

    positive_returns = sum(r for r in log_returns if r > 0)
    negative_returns = abs(sum(r for r in log_returns if r < 0))

    if positive_returns == 0:
        return 0
    elif negative_returns == 0:
        # Avoiding division by zero > float("inf")
        return round(ln(positive_returns / 0.01), 2)
    else:
        profit_ratio = positive_returns / negative_returns
        return round(max(ln(profit_ratio), 0), 2)


def martin_ratio(log_returns: list[float]) -> float:
    """
    Calculate the Martin ratio also known as Ulcer Performing Index (UPI) from a list of log returns.

    Parameters :
    -------
        - `log_returns` : List containing log returns for each candlestick

    Returns :
    -------
        - `float` : Non-negative martin ratio

    Note :
    -------
        - If there is no drawdowns, the martin ratio is calculated as the total return divided by 0.01
    """

    # Pattern needs to be matched at least 2.5% of the time (avoiding noise)
    pattern_matches = sum(1 for r in log_returns if isinstance(r, float))
    if pattern_matches < 0.025 * len(log_returns):
        return 0

    total_return = max(round(sum(log_returns), 2), 0)
    squared_drawdowns = [r**2 for r in log_returns if r < 0]

    if total_return == 0:
        return 0
    elif len(squared_drawdowns) == 0:
        # Avoiding division by zero > float("inf")
        return round(total_return / 0.01, 2)
    else:
        return round(total_return / sqrt(mean(squared_drawdowns)), 2)
