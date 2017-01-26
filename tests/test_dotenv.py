import os
import textwrap
import unittest
from tempfile import NamedTemporaryFile

from foil.dotenv import read_dotenv


def mock_dotenv():
    return textwrap.dedent("""\
SECRET=quiet
# comment this
forgot equals
DB='drawer'""")


class TestDotEnv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with NamedTemporaryFile(suffix='.env', delete=False) as tmp:
            with open(tmp.name, 'w', encoding='UTF-8') as file:
                file.write(mock_dotenv())
            cls.path = tmp.name

    def test_read_dotenv(self):
        expected = [('SECRET', 'quiet'), ('DB', 'drawer')]
        result = list(read_dotenv(self.path))

        self.assertEqual(expected, result)

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.path):
            os.unlink(cls.path)
