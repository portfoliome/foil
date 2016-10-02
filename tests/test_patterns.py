import re
import unittest

from foil.patterns import (
    match_subgroup, match_group, add_regex_start_end, tokenize_group_pattern
)


class TestPatternMatch(unittest.TestCase):
    def test_match_subgroup(self):
        element1 = r'(?P<element1>[A-Z])'
        element2 = r'(?P<element2>[0-9])'
        pattern = re.compile(element1 + r'_' + element2)
        sequence = ['A_1', '1_Z', 'B_2', 'C_#']

        expected = [
            {'element1': 'A', 'element2': '1'},
            {'element1': 'B', 'element2': '2'}
        ]

        result = list(match_subgroup(sequence, pattern))

        self.assertEqual(expected, result)


class TestReHelpers(unittest.TestCase):

    def test_match_group(self):
        result = match_group(['apple', 'orange', 'peach'])
        expected = 'apple|orange|peach'

        self.assertEqual(expected, result)

    def test_add_regex_start_end(self):
        # NOTE: purposely using one positional and one keyword arg in test.
        @add_regex_start_end
        def foo(currency, country='[A-Z]{2}'):
            return '{currency}_{country}'.format(currency=currency,
                                                 country=country)

        result = foo('USD')
        expected = '^USD_[A-Z]{2}$'

        self.assertEqual(expected, result)


class TestTokenizePattern(unittest.TestCase):

    def test_tokenize_group_pattern(self):
        token_name = 'greeting'
        choices = ['hello', 'bonjour']
        pattern = tokenize_group_pattern(token_name, choices)

        expected = {'greeting': 'bonjour'}
        result = re.match(pattern, 'bonjour').groupdict()

        self.assertEqual(expected, result)
