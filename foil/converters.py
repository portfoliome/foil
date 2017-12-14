from math import isnan, nan

from foil.records import replace_keys, rename_keys


def nan_to_none(value):
    return None if isnan(value) else value


def none_to_nan(value):
    return nan if value is None else value
