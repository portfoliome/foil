import unittest

from foil.util import natural_sort


class TestNaturalSort(unittest.TestCase):
    def test_natural_sort(self):
        entries = ['ab127b', 'ab123b']

        expected = ['ab123b', 'ab127b']
        result = natural_sort(entries)

        self.assertEqual(expected, result)
