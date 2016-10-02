"""
Utilities for filtering sequences.
"""

from itertools import product, chain
from operator import attrgetter, itemgetter
from typing import Dict, Generator, List, Tuple


class AttributeFilter:
    """
    Filter a sequence of objects/namedtuples by on attribute value predicates.

    Parameters
    ----------
    keys: group of attribute keys to use as filter set.
    predicates: values of attribute set to use in filtering.
    """

    slots = ('keys', 'predicates', 'indexer')

    def __init__(self, keys: Tuple[str], predicates: List[Tuple]):
        self.keys = keys
        self.predicates = set(predicates)
        self.indexer = attrgetter(*keys)

    def including(self, sequence) -> Generator:
        """Include the sequence elements matching the filter set."""
        return (element for element in sequence
                if self.indexer(element) in self.predicates)

    def excluding(self, sequence) -> Generator:
        """Exclude the sequence elements matching the filter set."""
        return (element for element in sequence
                if self.indexer(element) not in self.predicates)


def create_key_filter(properties: Dict[str, list]) -> List[Tuple]:
    """Generate combinations of key, value pairs for each key in properties.

    Examples
    --------
    properties = {'ent': ['geo_rev', 'supply_chain'], 'own', 'fi'}
    >> create_key_filter(properties)
      --> [('ent', 'geo_rev'), ('ent', 'supply_chain'), ('own', 'fi')]
    """

    combinations = (product([k], v) for k, v in properties.items())

    return chain.from_iterable(combinations)


def create_indexer(indexes: list):
    """Create indexer function to pluck values from list."""

    if len(indexes) == 1:
        index = indexes[0]
        return lambda x: (x[index],)
    else:
        return itemgetter(*indexes)
