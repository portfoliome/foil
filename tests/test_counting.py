import unittest

from foil.counting import count_by


class TestCounting(unittest.TestCase):
    def test_count_by(self):
        field_name = 'field'
        records = [{field_name: 'a'}, {field_name: 'b'}, {field_name: 'a'}]

        expected = {'a': 2, 'b': 1}
        result = count_by(records, field_name)
        self.assertDictEqual(expected, result)
