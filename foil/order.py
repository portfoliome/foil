from itertools import filterfalse, groupby, tee


def partition_ordered(sequence, key=None):
    """Partition ordered sequence by key.

    Sequence is expected to already be ordered.

    Parameters
    ----------
    sequence: iterable data.
    key: partition key function

    Yields
    -------
    iterable tuple(s) of partition key, data list pairs.

    Examples
    --------
    1. By object attributes.

    Partition sequence of objects by a height and weight attributes
    into an ordered dict.

    >> attributes = ('height', 'weight')
    >> OrderedDict(partition_ordered(sequence, attrgetter(*attributes)))

    2. By index items.

    Partition sequence by the first character index of each element.

    >> index = 0
    >> sequence = ['112', '124', '289', '220', 'Z23']
    >> list(partition_ordered(sequence, itemgetter(index)))
    """

    yield from ((k, list(g)) for k, g in groupby(sequence, key=key))


def partition(predicate, iterable):
    """Use a predicate to partition true and false entries.

    Reference
    ---------
    Python itertools documentation.
    """

    t1, t2 = tee(iterable)

    return filterfalse(predicate, t1), filter(predicate, t2)
