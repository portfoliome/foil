import collections
from functools import partial
from itertools import chain
from types import MappingProxyType
from typing import Callable
from uuid import UUID

import iso8601
from foil.parsers import parse_iso_date as _parse_iso_date


def parse_uuid(value):
    try:
        value = UUID(value, version=4)
    except ValueError:
        pass

    return value


def parse_iso_date(value):
    try:
        value = _parse_iso_date(value)
    except AttributeError:
        pass

    return value


def parse_iso_datetime(value):

    # Prevent iso8601 over-zealous datetime parsing
    if '-' in value and ':' in value:
        try:
            value = iso8601.parse_date(value)
        except iso8601.ParseError:
            pass

    return value


STRING_DECODERS = (parse_uuid, parse_iso_date, parse_iso_datetime)


def json_decoder_hook(dct, str_decoders=STRING_DECODERS,
                      converters=MappingProxyType(dict())) -> dict:
    """Decoder for parsing typical objects like uuid's and dates."""

    for k, v in dct.items():
        if k in converters:
            parse_func = converters[k]
            dct[k] = parse_func(v)

        elif isinstance(v, str):
            for decode_func in str_decoders:
                v = decode_func(v)

                if not isinstance(v, str):
                    break

            dct[k] = v
        elif isinstance(v, collections.Mapping):
            dct[k] = json_decoder_hook(v, str_decoders, converters)

    return dct


def make_json_decoder_hook(str_decoders=STRING_DECODERS,
                           extra_str_decoders=tuple(),
                           converters=MappingProxyType(dict())) -> Callable:
    """Customize JSON string decoder hooks.

    Object hook for typical deserialization scenarios.

    Notes
    -----
    Specifying a field in converters will ensure custom decoding/passthrough.

    Parameters
    ----------
    str_decoders: functions for decoding strings to objects.
    extra_str_decoders: appends additional string decoders to str_decoders.
    converters: field / parser function mapping.
    """

    str_decoders = tuple(chain(str_decoders, extra_str_decoders))
    object_hook = partial(json_decoder_hook, str_decoders=str_decoders,
                          converters=converters)

    return object_hook
