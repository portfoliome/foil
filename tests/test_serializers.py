import json
import unittest
import uuid
from datetime import date, datetime

from foil.serializers import json_serializer


class TestJSONSerializer(unittest.TestCase):

    def test_serialize_uuid(self):
        uid = uuid.uuid4()

        expected = '"{}"'.format(uid)
        result = self._serialize(uid)

        self.assertEquals(expected, result)

    def test_serialize_date(self):
        d = date(2014, 7, 14)

        expected = '"{}"'.format(d.strftime('%Y-%m-%d'))
        result = self._serialize(d)

        self.assertEquals(expected, result)

    def test_serialize_datetime(self):
        dt = datetime(2015, 3, 13, 20, 33, 22, 567)

        expected = '"{}Z"'.format(dt.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        result = self._serialize(dt)

        self.assertEquals(expected, result)

    def _serialize(self, obj):
        return json.dumps(obj, default=json_serializer)
