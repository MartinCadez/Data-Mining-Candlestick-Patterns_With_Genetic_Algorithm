"""
Module Name: pattern_evaluation.py
Description: Need to update!

Last Updated: 2024-09-01
"""

from math import log as ln
from statistics import mean

import pandas as pd


def pattern_is_matched(
    encoded_pattern: list[int],
    current_row: pd.Series,
    historical_window: pd.DataFrame,
    max_lag: int,
) -> bool:
    """
    Matches an encoded candlestick pattern against historical market price action chunk.

    Parameters :
    -------
        - `encoded_pattern` : List of integers representing the pattern to be matched
        - `current_row` : Representing the most recent candlestick, that is being evaluated
        - `historical_window` : DataFrame containing rows from the current candle minus `max_lag`
           up to the current candle (does not include the current candle)
        - `max_lag` : The maximum number of rows (candles) to look back in `historical_window`

    Returns :
    -------
        - `boolean` : True if the pattern is matched on a given row (candlestick), False otherwise
    """

    param_map = {0: "Open", 1: "Close", 2: "High", 3: "Low"}
    comparison_map = {0: "<", 1: ">"}

    # Ensure there's enough historical data to match the pattern
    if len(historical_window) < max_lag:
        return False

    # Validate every condition of the given pattern
    for i in range(0, len(encoded_pattern), 5):
        param1_type, lag1, comparison_type, param2_type, lag2 = encoded_pattern[
            i : i + 5
        ]
        param1 = param_map[param1_type]
        param2 = param_map[param2_type]
        comparison = comparison_map[comparison_type]
        price1 = (
            historical_window.iloc[-int(lag1)][param1]
            if int(lag1)
            else current_row[param1]
        )
        price2 = (
            historical_window.iloc[-int(lag2)][param2]
            if int(lag2)
            else current_row[param2]
        )

        if (comparison == "<" and price1 > price2) or (
            comparison == ">" and price1 < price2
        ):
            return False

    return True


def evaluate_candlestick_pattern(
    df: pd.DataFrame,
    encoded_pattern: list[int],
    max_lag: int,
    bullish_focus: bool = True,
) -> list[float]:
    """
    Evaluates a candlestick pattern against inserted market data.

    Parameters :
    -------
        - `df` : DataFrame containing time-series market data (price action).
                 Columns "Open", "Close", "High", "Low" need to be present
        - `encoded_pattern` : List of integers representing the pattern to be evaluated
        - `max_lag` : The maximum number of rows (candles) to look back in `df` from the reference row (candle)
        - `bullish_focus` : Boolean indicating whether to focus on bullish (True) or bearish (False) patterns

    Returns :
    -------
        - `log_returns` : List of log returns. If the pattern is matched, the natural logarithm of ratio from a "Close" price to an "Open" price is appended. Otherwise (if not matched) 0 is appended.


    Note :
    -------
        - If the pattern is matched on the last candle, the average of previous log returns is returned, since there is no subsequent row (candle) to calculate the log return.
    """

    log_returns = [0] * max_lag

    # Determine log returns for each row (candle) in the `df` (market data)
    for candle in range(max_lag, len(df)):
        row = df.iloc[candle]
        lookback_chunk = df.iloc[candle - max_lag : candle]

        if pattern_is_matched(encoded_pattern, row, lookback_chunk, max_lag):
            if candle + 1 < len(df):
                next_open = df.iloc[candle + 1]["Open"]
                next_close = df.iloc[candle + 1]["Close"]
                pattern_log_return = round(ln(next_close / next_open), 2)
                log_returns.append(
                    pattern_log_return if bullish_focus else -pattern_log_return
                )
            else:
                # Pattern matched on the last candle, return average log return
                non_zero_returns = [r for r in log_returns if r != 0]
                avg_return = round(mean(non_zero_returns), 2)
                log_returns.append(avg_return)
        else:
            log_returns.append(0)

    return log_returns
