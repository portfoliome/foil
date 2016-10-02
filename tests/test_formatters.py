import unittest

from foil.formatters import format_repr, format_repr_info


class Klass:
    def __init__(self, z, y):
        self.z = z
        self.y = y


class TestObjectReprFormatters(unittest.TestCase):
    def setUp(self):
        self.obj = Klass('hello', 10)
        self.attributes = ['z', 'y']

    def test_format_repr(self):
        result = format_repr(self.obj, self.attributes)
        expected = "Klass(z='hello', y=10)"

        self.assertEqual(expected, result)

    def test_format_repr_info(self):
        result = format_repr_info(self.obj, self.attributes)
        expected = "<Klass(z='hello', y=10)>"

        self.assertEqual(expected, result)
