import unittest
from collections import namedtuple
from foil.filters import AttributeFilter, create_key_filter, create_indexer


TeamRank = namedtuple('TeamRank', ['sport', 'team', 'rank'])


class TestAttributeFilter(unittest.TestCase):

    def setUp(self):
        self.teams = [TeamRank('baseball', 'cubs', 2),
                      TeamRank('basketball', 'bulls', 1),
                      TeamRank('baseball', 'mets', 1),
                      TeamRank('basketball', 'lakers', 2),
                      TeamRank('basketball', 'knicks', 3),
                      TeamRank('basketball', 'bulls', 2)]

    def test_include_attributes(self):
        keys = ('sport', 'team')
        include = [('basketball', 'bulls'),
                   ('basketball', 'knicks')]

        expected = [TeamRank('basketball', 'bulls', 1),
                    TeamRank('basketball', 'knicks', 3),
                    TeamRank('basketball', 'bulls', 2)]
        result = list(AttributeFilter(keys, predicates=include).including(self.teams))

        self.assertEqual(expected, result)

    def test_exclude_attributes(self):
        keys = ('sport', 'team', 'rank')
        remove = [('basketball', 'bulls', 2),
                  ('baseball', 'mets', 1),
                  ('basketball', 'lakers', 3)]

        expected = [
            TeamRank('baseball', 'cubs', 2),
            TeamRank('basketball', 'bulls', 1),
            TeamRank('basketball', 'lakers', 2),
            TeamRank('basketball', 'knicks', 3)]
        result = list(AttributeFilter(keys, predicates=remove).excluding(self.teams))

        self.assertEqual(expected, result)

    def test_create_key_filter(self):
        properties = {'sports': ['baseball', 'basketball'],
                      'teams': ['bulls', 'knicks', 'lakers']}

        expected = set([('sports', 'baseball'),
                        ('sports', 'basketball'),
                        ('teams', 'bulls'),
                        ('teams', 'knicks'),
                        ('teams', 'lakers')])
        result = set(create_key_filter(properties))

        self.assertSetEqual(result, expected)


class TestCreateIndexer(unittest.TestCase):

    def setUp(self):
        self.record = [0, 10, 20]

    def test_single_indexer(self):
        indexer = create_indexer([1])

        expected = (10,)
        result = indexer(self.record)

        self.assertEqual(expected, result)

    def test_multi_indexer(self):
        indexer = create_indexer([2, 0])

        expected = (20, 0)
        result = indexer(self.record)

        self.assertEqual(expected, result)
