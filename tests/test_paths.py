import os
import unittest
import zipfile
from tempfile import NamedTemporaryFile

from foil.paths import (match_files, match_file_listing,
                        get_file_listing_sha,
                        match_zipfile_members,
                        find_zipfile_member,
                        strip_full_path, merge_paths,
                        strip_file_listing, unique_listing_directories)


def mock_file_listing():
    return ['ABC_124.txt', 'RANDOM.txt', 'ABC_123.txt']


def mock_pattern():
    return r'ABC_[0-9]+.txt'


def mock_pattern_match():
    return ['ABC_124.txt', 'ABC_123.txt']


class TestMatchFiles(unittest.TestCase):

    def setUp(self):
        self.pattern = mock_pattern()

    def test_match_files(self):
        files = mock_file_listing()

        expected = set(mock_pattern_match())
        result = set(match_files(files, self.pattern))

        self.assertCountEqual(expected, result)

    def test_match_listings(self):
        paths = ['/home/ABC_124.txt', 'home/away/RANDOM.txt', 'ABC_123.txt']

        expected = set(['/home/ABC_124.txt', 'ABC_123.txt'])
        result = set(match_file_listing(paths, self.pattern))

        self.assertEqual(expected, result)


class TestZipPaths(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        filenames = mock_file_listing()

        with NamedTemporaryFile(prefix='zip_path_', suffix='.zip', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, mode='w') as myzip:
                for file in filenames:
                    myzip.writestr(file, b'')
            cls.zip_path = tmp.name

    def setUp(self):
        self.pattern = mock_pattern()

    def test_match_zipfile_members(self):

        expected = set(mock_pattern_match())
        result = set(match_zipfile_members(self.zip_path, self.pattern))

        self.assertEqual(expected, result)

    def test_find_zipfile_member(self):

        expected = mock_pattern_match()[0]
        result = find_zipfile_member(self.zip_path, self.pattern)

        self.assertEqual(expected, result)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.zip_path):
            os.unlink(cls.zip_path)


class TestSHA(unittest.TestCase):

    def test_get_file_listing_sha(self):
        from hashlib import sha256
        file_listings = ['/xyz/file2.zip', '/abc/file1.zip']

        expected = sha256(b'/abc/file1.zip' + b'/xyz/file2.zip').hexdigest()
        result = get_file_listing_sha(file_listings)

        self.assertEqual(expected, result)


class TestPathFormatters(unittest.TestCase):

    def setUp(self):
        self.directory = 'blah' + os.sep
        self.base_path = os.sep + self.directory

    def test_strip_full_path(self):

        expected = self.directory
        result = strip_full_path(self.base_path)

        self.assertEqual(expected, result)

    def test_merge_paths(self):
        directory_name = 'blah_sub_directory'
        sub_directory = os.sep + directory_name

        path2 = os.path.join(self.base_path, sub_directory)

        expected = os.path.join(self.base_path, directory_name)
        result = merge_paths(self.base_path, path2)

        self.assertEqual(expected, result)


class TestFileDirectoryListing(unittest.TestCase):

    def setUp(self):
        self.paths = ['/foobar/bar.zip', '/foobar/foo.txt', '/foobar/bar/foo.txt']

    def test_strip_file_listing(self):
        expected = ['/foobar', '/foobar', '/foobar/bar']
        result = list(strip_file_listing(self.paths))

        self.assertEqual(expected, result)

    def test_unique_listing_directories(self):
        expected = set(['/foobar', '/foobar/bar'])
        result = unique_listing_directories(self.paths)

        self.assertEqual(expected, result)
