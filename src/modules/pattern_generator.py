"""
Module Name: pattern_generator.py
Description: Need to update!

Last Updated: 2024-09-01
"""

import random
from typing import ClassVar, Set, Tuple


class CandlestickPatternGenerator:
    """
    Sets the foundation for generating encoded candlestick patterns.

    Attributes :
    -------
        - `max_lag`: Maximum number of candlesticks to look back for each parameter in a pattern
        - `num_conds`: Number of conditions of each pattern

    Class Variables :
    -------
        - `params`: List of candlestick parameters: ["O" (Open), "C" (Close), "H" (High), "L" (Low)].
        - `comparisons`: List of comparison operators: ["<" (less than), ">" (greater than)].

    Methods :
    -------
        - `get_patterns(num_patterns)`: Generates and returns a specified number of encoded candlestick patterns

    Example :
    -------
        - Example illustrates the generation of three encoded candlestick patterns

    .. code-block:: python
        # Create an instance of the CandlestickPatternGenerator class
        generator = CandlestickPatternGenerator(max_lag=3, num_conds=2)
        # Generate 3 encoded candlestick patterns
        encoded_patterns = generator.get_patterns(num_patterns=3)
        print(encoded_patterns)

    .. code-block:: text
        ----------------------OUTPUT----------------------
        [[1, 1, 1, 3, 0, 3, 0, 1, 3, 3],    # First pattern
        [2, 1, 1, 1, 2, 3, 1, 1, 3, 2],     # Second pattern
        [1, 3, 0, 2, 2, 3, 3, 1, 1, 0]]     # Third pattern

    .. code-block:: text
        ---------------------DECODED----------------------
        ['C[1] > L[0] & L[0] > L[3]',
        'H[1] > C[2] & L[1] > L[2]',
        'C[3] < H[2] & L[3] > C[0]']
    """

    params: ClassVar = ["O", "C", "H", "L"]
    comparisons: ClassVar = ["<", ">"]

    def __init__(self, max_lag: int, num_conds: int):
        self.max_candlestick_lookback = max_lag
        self.number_of_conditions = num_conds

    def get_patterns(self, num_patterns: int) -> list[list[int]]:
        """
        Generates and returns the specified number of encoded candlestick patterns.

        Parameters :
        -------
            - `num_patterns` : Number of patterns to generate

        Returns :
        -------
            - `encoded_patterns` : List containing candlestick patterns
        """

        encoded_patterns = []
        # Iterate over the number of patterns to create list of conditions for each pattern
        for _ in range(num_patterns):
            conditions = []
            conditions_set = set()  # Set to keep track of existing conditions
            # Continue generating conditions until the required number of conditions is met
            while len(conditions) < self.number_of_conditions:
                param1 = random.choice(self.params)
                lag1 = random.randint(0, self.max_candlestick_lookback)
                comparison = random.choice(self.comparisons)
                param2 = random.choice(self.params)
                lag2 = random.randint(0, self.max_candlestick_lookback)
                if self._is_condition_valid(
                    param1, lag1, comparison, param2, lag2, conditions_set
                ):
                    condition = (param1, lag1, comparison, param2, lag2)
                    conditions.append(condition)
                    conditions_set.add(condition)
            encoded_patterns.append(self._encode_pattern(conditions))
        return encoded_patterns

    @staticmethod
    def _is_condition_valid(
        param1: str,
        lag1: int,
        comparison: str,
        param2: str,
        lag2: int,
        conditions_set: Set[Tuple[str, int, str, str, int, str]],
    ) -> bool:
        """
        Checks if a generated condition is valid, unique, and logically rational.

        Parameters :
        -------
            - `param1` : First parameter (e.g., "O", "C", "H", "L")
            - `lag1` : Lookback period for the first parameter
            - `comparison` : Comparison operator ("<" or ">")
            - `param2` : Second parameter
            - `lag2` : Lookback period for the second parameter
            - `conditions_set` : Set of already existing conditions

        Returns :
        -------
            - `bool` : True if the condition is valid, False otherwise

        Condition Validation Examples:
        -------
            - The table below lists invalid conditions in the order they are evaluated in the code

            .. code-block:: text
                +-----------------------+---------------------------+
                | Invalidation Label    | Reference   | Rejection   |
                +-----------------------+---------------------------+
                | Duplication           | C[1] > L[3] | C[1] > L[3] |
                | Contradiction         | C[1] > L[3] | C[1] < L[3] |
                | Reverse Duplicated    | C[1] > L[3] | L[3] < C[1] |
                | Reverse Contradiction | C[1] > L[3] | L[3] > C[1] |
                | Redundant  H - L      |     ---     | H[0] > L[0] |
                | Redundant  L - H      |     ---     | L[0] < H[0] |
                | Redundant  HL - OC    |     ---     | H[0] > C[0] |
                | Redundant  OC - HL    |     ---     | O[0] > L[0] |
                | Adjacent O - C        |     ---     | O[0] < C[1] |
                | Adjacent C - O        |     ---     | C[2] < O[1] |
                | Self-Comparison       |     ---     | C[0] < C[0] |
                +-----------------------+---------------------------+

            - (Redundant  H - L) : "High" is always greater than "Low" on the same candle
            - (Redundant  HL - OC) : "High" is always greater than "Close" or Open (vice versa for "Low") on the same candle
            - (Adjacent O - C) : Previous "Close" is the same as the current "Open" for every candle
        """
        return (
            False
            if (
                {
                    (param1, lag1, comparison, param2, lag2),
                    (param2, lag2, comparison, param1, lag1),
                    (param2, lag2, ">" if comparison == "<" else "<", param1, lag1),
                    (param1, lag1, ">" if comparison == "<" else "<", param2, lag2),
                }
                & conditions_set
                or (
                    lag1 == lag2
                    and (
                        (param1 == "H" and param2 == "L")
                        or (param1 == "L" and param2 == "H")
                        or (param1 in ["H", "L"] and param2 in ["O", "C"])
                        or (param1 in ["O", "C"] and param2 in ["H", "L"])
                    )
                )
                or (
                    (param1 == "O" and param2 == "C" and lag1 == lag2 - 1)
                    or (param1 == "C" and param2 == "O" and lag1 == lag2 + 1)
                )
                or (param1 == param2 and lag1 == lag2)
            )
            else True
        )

    @staticmethod
    def _encode_pattern(conditions: list[Tuple[str, int, str, str, int]]) -> list[int]:
        """
        Encodes a list of candlestick conditions into a numeric format.

        Parameters :
        -------
            - `conditions` : List of conditions to encode. Each condition is represented as :
                             (`param1`, `lag1`, `comparison`, `param2`, `lag2`)

        Returns :
        -------
            - `encoded_pattern` : List of integers representing the encoded pattern

        Example :
        -------
            - Example illustrates encoding of candlestick pattern with two conditions

        .. code-block:: python
            Input : [("O", 0, ">", "C", 1), ("C", 1, "<", "O", 0)]
            Output : [1, 0, 1, 0, 1, 1, 1, 1, 0, 0]

        Note :
        -------
            - Length of the encoded pattern is always a multiple of 5 (5 integers per condition)
        """
        param_map = {"O": 0, "C": 1, "H": 2, "L": 3}
        comparison_map = {"<": 0, ">": 1}
        encoded_pattern = []
        for param1, lag1, comparison, param2, lag2 in conditions:
            encoded_pattern.extend(
                [
                    param_map[param1],
                    lag1,
                    comparison_map[comparison],
                    param_map[param2],
                    lag2,
                ]
            )
        return encoded_pattern
