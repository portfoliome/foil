import io
import os
import tempfile
import unittest
from unittest import mock
from urllib.parse import urljoin

from foil.ftp import (parse_line, ftp_walk, ftp_listing_paths, ListingType,
                      FTP_URL_TEMPLATE, download_ftp_url)


FILE_CONTENT = b'mock_content'

MOCK_FTP_CONFIG = {
    'user': 'fake_user',
    'password': 'fake_password',
    'host': 'host',
    'port': 21
}


def mock_directory_line(name):
    return 'drwxr-xr-x 4   ftsclient       ftsclient 60      Dec 11 10:03 {}'.format(name)


def mock_file_line(name):
    return '-rw-r--r-- 1   bd_mgr          online  3661980 Mar 30 02:13 {}'.format(name)


def mock_ftp_walk():
    return iter([('/root', ['directory1', 'directory2'], ['file1']),
                 ('/root/directory1', ['subdirectory'], []),
                 ('/root/directory1/subdirectory', [], ['file1', 'file2']),
                 ('/root/directory2', [], [])])


class MockFTPConnection:
    FTP_DIR_TREE = {
        '/root': [mock_directory_line('directory1'),
                  mock_directory_line('directory2'),
                  mock_file_line('file1')],
        '/root/directory1': [mock_directory_line('subdirectory')],
        '/root/directory1/subdirectory': [mock_file_line('file1'),
                                          mock_file_line('file2')],
        '/root/directory2': ['totals']}

    BINARY_DATA = {'file1': b'abc', 'file2': b'123'}

    def dir(self, path, callback):
        listings = self.FTP_DIR_TREE[path]
        for listing in listings:
            callback(listing)

    def retrbinary(self, path, callback):
        file = path.rpartition(' ')[-1]
        callback(self.BINARY_DATA[file])


def mock_url_open(url):
    return io.BytesIO(FILE_CONTENT)


class TestListingTraversal(unittest.TestCase):
    def setUp(self):
        self.conn = MockFTPConnection()
        self.root = '/root'

    def test_ftp_walk(self):
        expected = list(mock_ftp_walk())
        result = list(ftp_walk(self.conn, rootpath=self.root))

        self.assertEqual(expected, result)

    def test_ftp_listing_paths(self):
        expected = set(['/root/file1',
                        '/root/directory1/subdirectory/file1',
                        '/root/directory1/subdirectory/file2'])
        result = set(ftp_listing_paths(self.conn, self.root))

        self.assertEqual(expected, result)


class TestParseListingLines(unittest.TestCase):
    def test_parse_directory(self):
        directory_name = 'photos'
        entry = mock_directory_line(directory_name)

        expected = (ListingType.directory, directory_name)
        result = parse_line(entry)
        self.assertEqual(expected, result)

    def test_parse_file(self):
        filename = 'katies_photo_album.zip'
        entry = mock_file_line(filename)

        expected = (ListingType.file, filename)
        result = parse_line(entry)
        self.assertEqual(expected, result)


class TestFtpFileTransfer(unittest.TestCase):

    def setUp(self):
        self.filename = 'makeme.zip'
        self.ftp_url = FTP_URL_TEMPLATE.format_map(MOCK_FTP_CONFIG)
        self.source_uri = urljoin(self.ftp_url, 'some_dir/some_file.zip')

    @mock.patch('foil.ftp.urllib.request.urlopen')
    def test_create_target_directory(self, mock_urlopen):
        mock_urlopen.side_effect = mock_url_open

        with tempfile.TemporaryDirectory(prefix='ftp_trans_') as temp_directory:
            target_uri = os.path.join(temp_directory, 'some_dir', self.filename)

            download_ftp_url(self.source_uri, target_uri)

            with open(target_uri, 'rb') as result_file:
                result = result_file.read()

        self.assertEqual(FILE_CONTENT, result)

        if os.path.exists(temp_directory):
            os.unlink(temp_directory)
