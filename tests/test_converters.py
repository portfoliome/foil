import unittest
from math import isnan, nan

from foil.converters import nan_to_none, none_to_nan


class TestNanConverters(unittest.TestCase):

    def test_nan_to_none(self):
        self.assertIsNone(nan_to_none(nan))
        self.assertEqual(1, nan_to_none(1))

    def test_none_to_nan(self):
        self.assertTrue(isnan(none_to_nan(None)))
        self.assertEqual(1, none_to_nan(1))
