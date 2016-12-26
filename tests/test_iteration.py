import unittest

from foil.iteration import chunks


class TestChunks(unittest.TestCase):
    def test_chunks_generator(self):
        gen = range(0, 8)
        chunksize = 3
        grouped = chunks(gen, chunksize=chunksize)

        expected = [(0, 1, 2), (3, 4, 5), (6, 7)]
        result = list(tuple(g) for g in grouped)

        self.assertEqual(expected, result)

    def test_chunks_sequence(self):
        seq = list(range(0, 9))
        chunksize = 3
        grouped = chunks(seq, chunksize=chunksize)

        expected = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
        result = [tuple(g) for g in grouped]

        self.assertEqual(expected, result)
