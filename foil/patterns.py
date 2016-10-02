"""
Pattern matching utilities.
"""

import re
from functools import wraps
from typing import Iterable


def match_subgroup(sequence, pattern):
    """Yield the sub-group element dictionary that match a regex pattern."""

    for element in sequence:
        match = re.match(pattern, element)

        if match:
            yield match.groupdict()


def match_group(choices: Iterable) -> str:
    return '|'.join(choices)


def add_regex_start_end(pattern_function):
    """Decorator for adding regex pattern start and end characters."""

    @wraps(pattern_function)
    def func_wrapper(*args, **kwargs):
        return r'^{}$'.format(pattern_function(*args, **kwargs))
    return func_wrapper


def tokenize_group_pattern(name, choices):
    pattern = match_group(choices)
    return tokenize_pattern(name, pattern)


def tokenize_pattern(name, pattern):
    return '(?P<%s>%s)' % (name, pattern)
