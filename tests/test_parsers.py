import unittest
from datetime import date

from foil.parsers import (make_converters, parse_bool, passthrough,
                          parse_float, parse_int, parse_int_bool,
                          parse_iso_date, parse_numeric, parse_quoted_bool,
                          parse_quoted_float, parse_quoted_int,
                          parse_quoted_string, parse_quoted_numeric,
                          parse_broken_json)


class TestTextParsers(unittest.TestCase):
    def test_bool(self):
        mock_data = [('true', True), ('false', False),
                     ('1', True), ('0', False), ('', None)]

        for input_expected in mock_data:
            with self.subTest(input_expect=input_expected):
                result = parse_bool(input_expected[0])
                expected = input_expected[1]

                self.assertEqual(expected, result)

    def test_float(self):
        expected = 3.412
        result = parse_float('3.412')

        self.assertEqual(result, expected)

    def test_int(self):
        expected = 3
        result = parse_int('3')

        self.assertEqual(expected, result)

    def test_numeric_nan_none(self):
        nulls = ['']

        for val in nulls:
            with self.subTest(val=val):
                self.assertEqual(parse_numeric(float, val), None)

    def test_int_bool(self):
        mock_data = [(1, True), (0, False), (None, None)]

        for input_expected in mock_data:
            with self.subTest(input_expect=input_expected):
                result = parse_int_bool(input_expected[0])
                expected = input_expected[1]

                self.assertEqual(expected, result)

    def test_parse_iso_date(self):
        mock_data = [('2014-04-04', date(2014, 4, 4)), ('', None), (None, None)]

        for input_expected in mock_data:
            with self.subTest(input_expect=input_expected):
                result = parse_iso_date(input_expected[0])
                expected = input_expected[1]

                self.assertEqual(expected, result)

    def test_pass_through(self):
        expected = 123
        result = passthrough(expected)

        self.assertEqual(expected, result)

class TestQuotedTextParsers(unittest.TestCase):
    def test_bool(self):
        mock_data = [('"1"', True), ('"0"', False), ('""', None), ('', None)]

        for input_expected in mock_data:
            with self.subTest(input_expect=input_expected):
                result = parse_quoted_bool(input_expected[0])
                expected = input_expected[1]

                self.assertEqual(expected, result)

    def test_float(self):
        expected = 3.412
        result = parse_quoted_float('"3.412"')

        self.assertEqual(result, expected)

    def test_int(self):
        expected = 3
        result = parse_quoted_int('"3"')

        self.assertEqual(expected, result)

    def test_numeric_nan(self):
        nulls = ['""', '']

        for val in nulls:
            with self.subTest(val=val):
                self.assertEqual(parse_quoted_numeric(float, val), None)

    def test_parse_quoted_string(self):
        mock_data = [('""', None), ('"Hello"', 'Hello')]

        for input_expected in mock_data:
            with self.subTest(input_expect=input_expected):
                result = parse_quoted_string(input_expected[0])
                expected = input_expected[1]

                self.assertEqual(expected, result)


class Klass:
    pass


class TestMakeConverters(unittest.TestCase):
    def test_casting_functions(self):
        datatype_names = ['ticker', 'shares', 'price', 'bought', 'custom']
        inputted_types = [str, int, float, bool, Klass]
        expected_types = [passthrough, parse_int, parse_float,
                          parse_bool, Klass]
        inputted = dict(zip(datatype_names, inputted_types))

        expected = dict(zip(datatype_names, expected_types))
        result = make_converters(inputted)

        self.assertEqual(expected, result)


class TestJSONParsers(unittest.TestCase):
    def test_parse_broken_json(self):
        broken_json = '{success:true}'

        expected = {'success': True}
        result = parse_broken_json(broken_json)

        self.assertEqual(expected, result)
