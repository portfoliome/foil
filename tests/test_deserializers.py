import json
import unittest
from datetime import datetime
from uuid import UUID

import iso8601

from foil.deserializers import make_json_decoder_hook


def parse_foobar(value):
    if value == 'foobar':
        return True
    else:
        return value


class TestJSONDeserializer(unittest.TestCase):
    def test_json_decoder_hook(self):
        serialized_data = json.dumps(
            {'time': '2017-01-19T21:41:18.056446Z',
             'date': '2013-04-05', 'date_str': '2013-04-05',
             'non_date': '8570', 'id': '060444c9-e2d7-4a55-964d-e495f2d5527f',
             'description': 'foo', 'data': {'count': 4},
             'foobar_field': 'foobar'}
        )
        converters = {'date_str': str}
        extra_decoders = (parse_foobar,)
        object_hook = make_json_decoder_hook(
            converters=converters, extra_str_decoders=extra_decoders
        )

        expected = {
            'time': datetime(2017, 1, 19, 21, 41, 18, 56446,
                             tzinfo=iso8601.UTC),
            'date': datetime(2013, 4, 5).date(),
            'date_str': '2013-04-05', 'non_date': '8570',
            'id': UUID('060444c9-e2d7-4a55-964d-e495f2d5527f', version=4),
            'description': 'foo', 'data': {'count': 4}, 'foobar_field': True
        }
        result = json.loads(serialized_data, object_hook=object_hook)

        self.assertEqual(expected, result)

    def test_nested_converters(self):
        serialized_data = json.dumps(
            {'time': {'date': '2014-04-01', 'time': '03:33:23'}}
        )
        converters = {'date': str}
        object_hook = make_json_decoder_hook(converters=converters)

        expected = {'time': {'date': '2014-04-01', 'time': '03:33:23'}}
        result = json.loads(serialized_data, object_hook=object_hook)

        self.assertEqual(expected, result)
