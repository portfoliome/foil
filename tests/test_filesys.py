import os
import unittest
from tempfile import NamedTemporaryFile
from uuid import uuid4

from foil.filesys import file_exists


class TestFileExists(unittest.TestCase):

    def setUp(self):
        with NamedTemporaryFile(prefix='mocke_', suffix='.txt',
                                delete=False) as tmp:
            with open(tmp.name, 'w') as fp:
                fp.write('121XZTT')

        self.tmp_path = tmp.name

    def test_file_exists(self):
        self.assertTrue(file_exists(self.tmp_path))

    def test_not_exists(self):
        file_name = str(uuid4()) + '.txt'

        with self.assertRaises(FileExistsError):
            file_exists(file_name)

    def tearDown(self):
        if os.path.exists(self.tmp_path):
            os.unlink(self.tmp_path)
