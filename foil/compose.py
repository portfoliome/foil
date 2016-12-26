from itertools import accumulate, product, repeat
from typing import Sequence, Generator, Iterable


def create_quantiles(items: Sequence, lower_bound, upper_bound):
    """Create quantile start and end boundaries."""

    interval = (upper_bound - lower_bound) / len(items)

    quantiles = ((g, (x - interval, x)) for g, x in
                 zip(items, accumulate(repeat(interval, len(items)))))

    return quantiles


def tupleize(element, ignore_types=(str, bytes)):
    """Cast a single element to a tuple."""
    if hasattr(element, '__iter__') and not isinstance(element, ignore_types):
        return element
    else:
        return tuple((element,))


def cartesian_product(sets):
    """Generate the cartesian product/cross product for
     2-tuple(2 fold cartesian product) sets.

    Examples
    >> cartesian_product('a', (1, 2)) -> ('a', 1), ('a', 2)
    >> cartesian_product((('b', 'c'), ('x', 'y')) ->
    >> ('b', 'x'), ('b', 'y'), ('c', 'x'), ('c', 'y')
    """

    return product(*(tupleize(element) for element in sets))


def disjoint_union(iterators) -> Iterable:
    """Join disjoint sets as an iterable stream."""
    for iterator in iterators:
        yield from iterator


def dictionize(fields: Sequence, records: Sequence) -> Generator:
    """Create dictionaries mapping fields to record data."""

    return (dict(zip(fields, rec)) for rec in records)


def flip_dict(d: dict) -> dict:
    return {v: k for k, v in d.items()}


def flip_iterable_dict(d: dict) -> dict:
    """Transform dictionary to unpack values to map to respective key."""

    value_keys = disjoint_union((cartesian_product((v, k))
                                 for k, v in d.items()))
    return dict(value_keys)
