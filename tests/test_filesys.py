import os
import shutil
import unittest
from tempfile import NamedTemporaryFile, mkdtemp
from uuid import uuid4

from foil.filesys import file_exists, ensure_file_directory


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


class TestEnsureFiles(unittest.TestCase):

    def setUp(self):
        self.base_path = mkdtemp()

    def test_ensure_file_directory(self):
        directory = str(uuid4())
        file_name = str(uuid4()) + '.txt'
        directory_path = os.path.join(self.base_path, directory)
        path = os.path.join(directory_path, file_name)

        ensure_file_directory(path)

        self.assertTrue(os.path.exists(directory_path))

        # make sure nothing happens on second call
        ensure_file_directory(path)

    def tearDown(self):
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)
