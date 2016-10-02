import unittest

from foil.compose import (tupleize, cartesian_product, disjoint_union,
                          create_quantiles, flip_dict, flip_iterable_dict)


class TestCartesianProduct(unittest.TestCase):

    def test_tupleize(self):
        elementlist = [None, 5,
                       'string', ('string',),
                       ('a', 'b', 'c')]

        expectedlist = [(None,), (5,),
                        ('string',), ('string',),
                        ('a', 'b', 'c')]

        for element, expected in zip(elementlist, expectedlist):
            with self.subTest(element=element):
                result = tupleize(element)
                self.assertEqual(result, expected)

    def test_carteisian_product(self):
        sets = (('a', 'bee', None), 'a')

        expected = [('a', 'a'), ('bee', 'a'), (None, 'a')]
        result = list(cartesian_product(sets))

        self.assertEqual(expected, result)

        sets = (('b', 'c'), ('x', 'y'))

        expected = [('b', 'x'), ('b', 'y'), ('c', 'x'), ('c', 'y')]
        result = list(cartesian_product(sets))

        self.assertEqual(expected, result)

    def test_disjoint_union(self):
        iter1 = iter([('a', 'a'), ('bee', 'a')])
        iter2 = iter([('z', None), ('zz', None)])

        expected = [('a', 'a'), ('bee', 'a'), ('z', None), ('zz', None)]
        result = list(disjoint_union([iter1, iter2]))

        self.assertEqual(expected, result)


class TestQuantiles(unittest.TestCase):

    def test_create_quantiles(self):
        items = ['a', 'b', 'c']
        lower_bound = 0.
        upper_bound = 6.

        expected = [('a', (0., 2.)), ('b', (2., 4.)), ('c', (4., 6.))]
        result = list(create_quantiles(items, lower_bound, upper_bound))

        self.assertEqual(expected, result)


class TestDictUtils(unittest.TestCase):

    def test_flip_dict(self):
        dictionary = {'a': 'aa', 'b': 'bb'}

        expected = {'aa': 'a', 'bb': 'b'}
        result = flip_dict(dictionary)

        self.assertEqual(expected, result)

    def test_flip_iterable_dict(self):
        dictionary = {'a': ['1', '2'], 'b': ['10', '20']}

        expected = {'1': 'a', '2': 'a', '10': 'b', '20': 'b'}
        result = flip_iterable_dict(dictionary)

        self.assertEqual(expected, result)
