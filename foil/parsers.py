"""Parsing utilities for ETL loading."""

from datetime import date
from decimal import Decimal
from functools import partial

import yaml

from foil.dates import parse_date


# Boolean string types, empty values for bool casting.
boolean_strings = {
    '1': True,
    '0': False,
    'true': True,
    'false': False,
    '': None,
    None: None
}

INT_TO_BOOL = {1: True, 0: False}


def passthrough(value):
    """Pass through value for no conversion."""
    return value


def parse_numeric(cast_function, value):
    if value is None or value is '':
        return None
    else:
        return cast_function(value)


# Numeric Parsers
parse_int = partial(parse_numeric, int)
parse_float = partial(parse_numeric, float)
parse_decimal = partial(parse_numeric, Decimal)


def parse_bool(value):
    return boolean_strings[value]


def parse_int_bool(value):
    if value is None:
        return None
    else:
        return INT_TO_BOOL[value]

# ----------------------------------------------------------
# Parsers for quoted text
# ----------------------------------------------------------


def unquote(value):
    """Removes left most and right most quote for str parsing."""

    return value.lstrip('"').rstrip('"')


def parse_quoted_numeric(cast_function, value):
    if value is '' or value == '""':
        return None
    else:
        return cast_function(value.replace('"', '', 2))


parse_quoted_int = partial(parse_quoted_numeric, int)
parse_quoted_float = partial(parse_quoted_numeric, float)
parse_quoted_decimal = partial(parse_quoted_numeric, Decimal)


def parse_iso_date(value):
    if value is None or value is '':
        return None
    else:
        return parse_date(value)


def parse_quoted_string(value):
    if value == '""':
        return None
    else:
        return unquote(value)


def parse_quoted_bool(value):
    return parse_bool(unquote(value))


TYPE_CASTERS = {
    str: passthrough,
    int: parse_int,
    float: parse_float,
    bool: parse_bool,
    date: parse_iso_date,
}


def make_converters(data_types) -> dict:
    """
    Return a mapping between data type names, and casting functions,
    or class definitions to convert text into its Python object.
    Parameters
    ----------
    data_types: dict-like
        data field name str: python primitive type or class.
    Example
    -------
    >> make_converters({'student': str, 'score': float, 'grade': Grade) ->
    {'student_name': passthrough, 'score': parse_float, 'grade': Grade)
    """

    return {k: TYPE_CASTERS.get(v, v) for k, v in data_types.items()}


def parse_broken_json(json_text: str) -> dict:
    """
    Parses broken JSON that the standard Python JSON module cannot parse.

    Ex: {success:true}

    Keys do not contain quotes and the JSON cannot be parsed using the regular json encoder.
    YAML happens to be a superset of JSON and can parse json without quotes.
    """

    # Add spacing between Key and Value to prevent parsing error
    json_text = json_text.replace(":", ": ")
    json_dict = yaml.load(json_text)

    return json_dict
