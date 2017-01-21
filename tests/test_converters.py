import unittest

from foil.converters import rename_keys, replace_keys


class TestKeyConverters(unittest.TestCase):
    def setUp(self):
        self.record = {'a': 1, 'b': 2, 'c': 3}
        self.key_map = {'a': 'aa', 'c': 'cc'}

    def test_rename_keys(self):
        expected = {'aa': 1, 'b': 2, 'cc': 3}
        result = rename_keys(self.record, key_map=self.key_map)

        self.assertEqual(expected, result)

    def test_replace_keys(self):
        expected = {'aa': 1, 'cc': 3}
        result = replace_keys(self.record, key_map=self.key_map)

        self.assertEqual(expected, result)
