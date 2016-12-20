import unittest

from foil.strings import camel_to_snake, snake_to_camel


class TestSnakeCamel(unittest.TestCase):

    def test_camel_to_snake_case(self):
        expected = 'hello_world'
        result = camel_to_snake('helloWorld')

        self.assertEqual(expected, result)

    def test_snake_to_camel_case(self):
        expected = '123HelloWorld'
        result = snake_to_camel('123_hello_world')

        self.assertEqual(expected, result)
