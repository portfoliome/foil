import csv
import io
import os
import unittest
import textwrap
import zipfile
from collections import namedtuple
from datetime import date, datetime
from tempfile import NamedTemporaryFile

from foil.fileio import (concatenate_streams, DelimitedReader,
                         DelimitedSubsetReader, ZipReader)


sample_path = os.path.join(os.path.dirname(__file__), 'sample_data')


class MockDialect(csv.Dialect):
    delimiter = '|'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_MINIMAL


def delimited_text():
    file_content = textwrap.dedent(r"""
"NAME"|"CLASS"|"DATE"|"ASSIGNMENT"|"SCORE"|"AVERAGE"
"Dave"|"American History"|2015-03-02|"QUIZ 1"|82|82.0
"Dave"|"American History"|2015-04-04|"QUIZ 2"|91|86.5
"Dave"|"American History"|2015-04-20|"Mid-term"|77|83.333
""").strip()
    return file_content


def data_records(fields):
    Record = namedtuple('Record', fields)
    records = [
        Record('Dave', 'American History', date(2015, 3, 2), 'QUIZ 1', 82.0, 82.0),
        Record('Dave', 'American History', date(2015, 4, 4), 'QUIZ 2', 91.0, 86.5),
        Record('Dave', 'American History', date(2015, 4, 20), 'Mid-term', 77.0, 83.333)]

    return records


def partial_data_records(fields):
    Record = namedtuple('Record', fields)
    records = [
        Record('Dave', 'American History', 82.0),
        Record('Dave', 'American History', 86.5),
        Record('Dave', 'American History', 83.333)]

    return records


def single_field_records(fields):
    Record = namedtuple('Record', fields)
    records = [Record('Dave'), Record('Dave'), Record('Dave')]

    return records


def parse_date(date_str):
    if date_str is '':
        return None
    else:
        return datetime.strptime(date_str, '%Y-%m-%d').date()


class TestDelimitedReader(unittest.TestCase):

    encoding = 'UTF-8'
    zip_filename = 'delimited_file1.txt'

    @classmethod
    def setUpClass(cls):
        file_content = delimited_text()
        with NamedTemporaryFile(prefix='delim_', suffix='.txt', delete=False) as tmp:
            with open(tmp.name, 'w', encoding='UTF-8') as text_file:
                text_file.write(file_content)
            cls.path = tmp.name

        file_content_bytes = bytes(file_content, cls.encoding)
        with NamedTemporaryFile(prefix='zipped_', suffix='.zip', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, mode='w') as myzip:
                myzip.writestr(cls.zip_filename, file_content_bytes)
            cls.zip_path = tmp.name

    def setUp(self):
        self.maxDiff = None
        self.fields = ['NAME', 'CLASS', 'DATE', 'ASSIGNMENT', 'SCORE', 'AVERAGE']
        self.converters = [str, str, parse_date, str, float, float]
        self.dialect = MockDialect()
        self.expected = data_records(self.fields)

    def test_stream_reader(self):
        stream = io.StringIO(delimited_text())
        reader = DelimitedReader(stream, dialect=self.dialect,
                                 fields=self.fields,
                                 converters=self.converters)

        result = list(reader)

        self.assertSequenceEqual(self.expected, result)

    def test_from_file(self):
        reader = DelimitedReader.from_file(path=self.path,
                                           encoding=self.encoding,
                                           dialect=self.dialect,
                                           fields=self.fields,
                                           converters=self.converters)

        result = list(reader)

        self.assertSequenceEqual(self.expected, result)

    def test_from_zipfile(self):
        reader = DelimitedReader.from_zipfile(path=self.zip_path,
                                              filename=self.zip_filename,
                                              encoding=self.encoding,
                                              dialect=self.dialect,
                                              fields=self.fields,
                                              converters=self.converters)

        result = list(reader)

        self.assertSequenceEqual(self.expected, result)

    def test_line_number(self):
        # counts skipped header line
        stream = io.StringIO(delimited_text())
        reader = DelimitedReader(stream, dialect=self.dialect,
                                 fields=self.fields,
                                 converters=self.converters)
        next(reader)
        next(reader)
        self.assertEqual(reader.file_line_number, 3)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.path):
            os.unlink(cls.path)

        if os.path.exists(cls.zip_path):
            os.unlink(cls.zip_path)


class TestDelimitedSubsetReader(unittest.TestCase):

    encoding = 'UTF-8'
    zip_filename = 'delimited_file1.txt'

    @classmethod
    def setUpClass(cls):
        file_content = delimited_text()
        with NamedTemporaryFile(prefix='delim_', suffix='.txt', delete=False) as tmp:
            with open(tmp.name, 'w', encoding='UTF-8') as text_file:
                text_file.write(file_content)
            cls.path = tmp.name

        file_content_bytes = bytes(file_content, cls.encoding)
        with NamedTemporaryFile(prefix='zipped_', suffix='.zip', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, mode='w') as myzip:
                myzip.writestr(cls.zip_filename, file_content_bytes)
            cls.zip_path = tmp.name

    def setUp(self):
        self.maxDiff = None
        self.headers = ['NAME', 'CLASS', 'DATE', 'ASSIGNMENT', 'SCORE', 'AVERAGE']
        self.fields = ['NAME', 'CLASS', 'AVERAGE']
        self.field_index = [self.headers.index(field) for field in self.fields]
        self.converters = [str, str, float]
        self.dialect = MockDialect()
        self.expected = partial_data_records(self.fields)

    def test_stream_reader(self):
        stream = io.StringIO(delimited_text())
        reader = DelimitedSubsetReader(stream,
                                       dialect=self.dialect,
                                       fields=self.fields,
                                       converters=self.converters,
                                       field_index=self.field_index)

        result = list(reader)

        self.assertSequenceEqual(self.expected, result)

    def test_from_file(self):
        reader = DelimitedSubsetReader.from_file(path=self.path,
                                                 encoding=self.encoding,
                                                 dialect=self.dialect,
                                                 fields=self.fields,
                                                 converters=self.converters,
                                                 field_index=self.field_index)

        result = list(reader)

        self.assertSequenceEqual(self.expected, result)

    def test_from_zipfile(self):
        reader = DelimitedSubsetReader.from_zipfile(path=self.zip_path,
                                                    filename=self.zip_filename,
                                                    encoding=self.encoding,
                                                    dialect=self.dialect,
                                                    fields=self.fields,
                                                    converters=self.converters,
                                                    field_index=self.field_index)

        result = list(reader)

        self.assertSequenceEqual(self.expected, result)

    def test_single_field(self):
        stream = io.StringIO(delimited_text())
        field_index = [0]
        fields = [self.fields[index] for index in field_index]
        converters = [self.converters[index] for index in field_index]

        reader = DelimitedSubsetReader(stream,
                                       dialect=self.dialect,
                                       fields=fields,
                                       converters=converters,
                                       field_index=field_index)

        expected = single_field_records(fields)
        result = list(reader)

        self.assertEqual(expected, result)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.path):
            os.unlink(cls.path)

        if os.path.exists(cls.zip_path):
            os.unlink(cls.zip_path)


class TestZipReader(unittest.TestCase):

    encoding = 'UTF-8'
    filename = 'sample_file.txt'
    file_content = 'abc\neasy\n123.\n'
    file_content_bytes = bytes(file_content, encoding=encoding)

    @classmethod
    def setUpClass(cls):
        with NamedTemporaryFile(prefix='zipped_', suffix='.zip', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, mode='w') as myzip:
                    myzip.writestr(cls.filename, cls.file_content_bytes)
            cls.path = tmp.name

    def test_read(self):
        result = ZipReader(self.path, self.filename).read(self.encoding)

        self.assertEqual(self.file_content, result)

    def test_readlines(self):
        line_gen = ZipReader(self.path, self.filename).readlines(self.encoding)
        expected = ['abc', 'easy', '123.']

        self.assertEqual(expected, list(line_gen))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.path):
            os.unlink(cls.path)


class TestConcatenateStreams(unittest.TestCase):
    def test_concatenate_streams(self):
        streams = [[1, 2, 3], ['a', 'b', 'c']]

        expected = [1, 2, 3, 'a', 'b', 'c']
        result = list(concatenate_streams(streams))

        self.assertEqual(expected, result)
