import unittest

from foil.agent import UserAgent


class TestAgent(unittest.TestCase):
    def test_user_agent(self):
        expected = 'Mozilla/4.0 (compatible; MSIE 4.01; Windows 95)'
        result = UserAgent.ie

        self.assertEqual(expected, result)
