import re

_RE_INT = re.compile(r'([0-9]+)')


def alphanum_key(s):
    """Turn a string into a list of string and number chunks.

        "z23a" -> ["z", 23, "a"]
        """

    return [int(c) if c.isdigit() else c for c in _RE_INT.split(s)]


def natural_sort(l):
    """Sort list based on alphanumeric key."""

    return sorted(l, key=alphanum_key)


def find_index(search_list, items):
    return [search_list.index(i) for i in items]
