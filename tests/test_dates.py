from datetime import datetime, date

import pytz
import unittest

from foil.dates import parse_date, DateTimeParser, _datetime_to_tuple


test_dt_data = [
    ('2015-04-03', datetime(2015, 4, 3)),
    ('2015-04-03T06:34:22', datetime(2015, 4, 3, 6, 34, 22)),
    ('2015-04-03T06:34:22.234', datetime(2015, 4, 3, 6, 34, 22, 234000)),
    ('2014-06-29T02:25:20 EST', datetime(2014, 6, 29, 6, 25, 20, tzinfo=pytz.utc)),
    ('2013-02-07T09:34:22 EDT', datetime(2013, 2, 7, 14, 34, 22, tzinfo=pytz.utc))]


def dt_dict():
    return dict(year='2014', month='07', day='03', hour='13',
                minute='02', second='45', microsecond='321')


class TestToolsDates(unittest.TestCase):

    def setUp(self):
        self.dt_dict = dt_dict()

    def test_factset_time_pattern(self):
        date_parser = DateTimeParser()

        for t in test_dt_data:
            data = t[0]
            expected = t[1]
            result = date_parser.parse(data)
            with self.subTest(data=data):
                self.assertEqual(expected, result)

    def test_parse_date(self):
        expected = date(2015, 4, 3)
        result = parse_date('2015-04-03')

        self.assertEqual(expected, result)

    def test_all_string_components(self):
        expected = (2014, 7, 3, 13, 2, 45, 321)
        result = _datetime_to_tuple(self.dt_dict)

        self.assertEqual(expected, result)

    def test_null_microsecond(self):
        self.dt_dict['microsecond'] = None

        expected = (2014, 7, 3, 13, 2, 45, 0)
        result = _datetime_to_tuple(self.dt_dict)

        self.assertEqual(expected, result)

    def test_no_microsecond(self):
        self.dt_dict['hour'] = None

        expected = (2014, 7, 3, 0, 2, 45, 321)
        result = _datetime_to_tuple(self.dt_dict)

        self.assertEqual(expected, result)

    def test_fail_no_month(self):
        self.dt_dict['month'] = None

        with self.assertRaises(TypeError):
            _datetime_to_tuple(dt_dict)
