import unittest

from collections import namedtuple
from operator import attrgetter, itemgetter

from foil.order import partition_ordered

MockTuple = namedtuple('MockTuple', ('a', 'b'))


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
