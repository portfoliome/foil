import unittest


from foil.records import inject_nulls, replace_keys, rename_keys


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


class TestInjectNulls(unittest.TestCase):
    def test_inject_nulls(self):
        record = {'city': 'Chicago'}
        record_copy = record.copy()
        field_names = ['city', 'state']

        expected = {'city': 'Chicago', 'state': None}
        result = inject_nulls(record, field_names)

        self.assertEqual(expected, result)
        self.assertEqual(record_copy, record)
