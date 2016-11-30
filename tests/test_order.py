import unittest

from collections import namedtuple
from operator import attrgetter, itemgetter

from foil.order import partition_ordered, partition

MockTuple = namedtuple('MockTuple', ('a', 'b'))


def is_even(x):
    return True if x % 2 == 0 else False


class TestPartitionOrdered(unittest.TestCase):

    def test_partition_by_attribute(self):

        data = [{'a': 5, 'b': 8}, {'a': 5, 'b': 7}, {'a': 4, 'b': 4}]
        tups = [MockTuple(**d) for d in data]

        expected = [(5, [MockTuple(a=5, b=8), MockTuple(a=5, b=7)]),
                    (4, [MockTuple(a=4, b=4)])]
        result = list(partition_ordered(tups, key=attrgetter('a')))

        self.assertSequenceEqual(expected, result)

    def test_partition_by_item(self):
        data = ['123', '234', '221', '210', '780', '822']

        expected = [('1', ['123']),
                    ('2', ['234', '221', '210']),
                    ('7', ['780']),
                    ('8', ['822'])]
        result = list(partition_ordered(data, key=itemgetter(0)))

        self.assertEqual(expected, result)


class TestPartition(unittest.TestCase):
    def test_partition(self):
        expected_true = [0, 2]
        expected_false = [1, 3]
        result_false, result_true = partition(is_even, range(0, 4))

        self.assertEqual(expected_true, list(result_true))
        self.assertEqual(expected_false, list(result_false))

