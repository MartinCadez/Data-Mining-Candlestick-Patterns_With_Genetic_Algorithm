"""
Module Name: pattern_encoder.py
Description: Need to update!

Last Updated: 2024-09-01
"""

import re


def encode_patterns(decoded_patterns: list[str]) -> list[list[int]]:
    """
    Encode a list of string-encoded patterns into a numerical format.

    Parameters :
    -------
        - `decoded_patterns` : List of strings where each string represents a pattern

    Returns :
    -------
        - `encoded_patterns` : List where each sublist containing integers represents an encoded version of the input patterns

    Example :
    -------
        - Example illustrates encoding of two decoded patterns where each pattern has three conditions

    .. code-block:: python
        decoded_patterns = [
            'H[0] < C[2] & O[0] > C[0] & H[1] > O[3]',  # First pattern
            'O[3] < O[0] & C[3] > O[3] & H[1] < O[3]'   # Second pattern
        ]
        encoded_patterns = encode_patterns(decoded_patterns)
        print(encoded_patterns)
        ----------------------OUTPUT----------------------
        [[2, 0, 0, 1, 2, 0, 0, 1, 1, 0, 2, 1, 1, 0, 3], # First pattern
        [0, 3, 0, 0, 0, 1, 3, 1, 0, 3, 2, 1, 0, 0, 3]]  # Second pattern
    """

    param_map = {"O": 0, "C": 1, "H": 2, "L": 3}
    comparison_map = {"<": 0, ">": 1}
    encoded_patterns = []

    condition_compiler = re.compile(
        r"(?P<param1>\w)\[(?P<lag1>\d+)\] (?P<comparison>[<>]) (?P<param2>\w)\[(?P<lag2>\d+)\]"
    )

    for pattern in decoded_patterns:
        conditions = pattern.split(" & ")
        encoded_pattern = []

        for condition in conditions:
            match = condition_compiler.match(condition)
            if match:
                encoded_pattern.extend(
                    [
                        param_map[match.group("param1")],
                        int(match.group("lag1")),
                        comparison_map[match.group("comparison")],
                        param_map[match.group("param2")],
                        int(match.group("lag2")),
                    ]
                )
        encoded_patterns.append(encoded_pattern)

    return encoded_patterns


def decode_patterns(encoded_patterns: list[list[int]]) -> list[str]:
    """
    Decodes a list of encoded patterns into a human-readable format.

    Parameters :
    -------
        - encoded_patterns : List where each sublist containing integers represents a pattern

    Returns :
    -------
        - decoded_patterns : List where each sublist containing integers represents an encoded version of the input patterns

    Example :
    -------
        - Example illustrates decoding of two encoded patterns where each pattern has three conditions
    .. code-block:: python
        encoded_patterns =  [
            [2, 0, 0, 1, 2, 0, 0, 1, 1, 0, 2, 1, 1, 0, 3],  # First pattern
            [0, 3, 0, 0, 0, 1, 3, 1, 0, 3, 2, 1, 0, 0, 3]   # Second pattern
        ]
        decoded_patterns = decode_patterns(encoded_patterns)
        print(decoded_patterns)
        ----------------------OUTPUT----------------------
        ['H[0] < C[2] & O[0] > C[0] & H[1] > O[3]',  # First pattern
        'O[3] < O[0] & C[3] > O[3] & H[1] < O[3]']   # Second pattern
    """

    param_map = {0: "O", 1: "C", 2: "H", 3: "L"}
    comparison_map = {0: "<", 1: ">"}
    decoded_patterns = []

    for pattern in encoded_patterns:
        conditions = []
        for i in range(0, len(pattern), 5):
            param1 = param_map[pattern[i]]
            lag1 = pattern[i + 1]
            comparison = comparison_map[pattern[i + 2]]
            param2 = param_map[pattern[i + 3]]
            lag2 = pattern[i + 4]
            conditions.append(f"{param1}[{lag1}] {comparison} {param2}[{lag2}]")
        decoded_patterns.append(" & ".join(conditions))

    return decoded_patterns
