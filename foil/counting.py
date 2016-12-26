from collections import defaultdict
from typing import Dict, Sequence


def count_by(records: Sequence[Dict], field_name: str) -> defaultdict:
    """
    Frequency each value occurs in a record sequence for a given field name.
    """

    counter = defaultdict(int)

    for record in records:
        name = record[field_name]
        counter[name] += 1

    return counter
