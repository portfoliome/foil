from collections import deque
from itertools import chain, islice


def chunks(items, chunksize):
    """Turn generator sequence into sequence of chunks."""

    items = iter(items)
    for first in items:
        chunk = chain((first,), islice(items, chunksize - 1))
        yield chunk
        deque(chunk, 0)
