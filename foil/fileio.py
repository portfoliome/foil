"""
tools.fileio.py contains helper utilities for file reading and writing.
"""

import csv
from collections import namedtuple
from contextlib import contextmanager
from io import BufferedReader
from zipfile import ZipFile

from foil.filters import create_indexer


class TextReader:
    """Reads text file.

    Parameters
    ----------
    path : Absolute path to text file.
    encoding : File encoding.
    """

    def __init__(self, path: str, encoding: str):
        self.path = path
        self.encoding = encoding

    def __iter__(self):
        with open(self.path, 'r', encoding=self.encoding) as f:
            for line in f:
                yield line.strip('\r\n')


class DelimitedReader:
    """Read delimited text stream into namedtuple Records.

    Attributes
    ----------
    stream: stream of text.
    dialect: delimited file attributes.
    fields: Record field names.
    converters: casting functions to cast fields to Python objects.
      Utilize tools.parsers.make_converters for the general use case.

    Factory Methods
    ---------------
    See factory methods for alternative constructors.

    Notes
    -----
    Previewing file header columns without loading, or extracting a large
    file can be accomplished by:
      >> DelimitedReader(params, fields=[], converters=[]).header -> header
    """

    def __init__(self, stream,
                 dialect: csv.Dialect, fields: list, converters: list):
        reader = csv.reader(stream, dialect=dialect)
        self.header = next(reader)
        self.reader = reader
        self.converters = converters
        self.Record = namedtuple('Record', fields)

    def __iter__(self):
        return self

    def __next__(self):
        Record = self.Record
        record = Record._make(type_converter(item) for type_converter, item
                              in zip(self.converters, next(self.reader)))
        return record

    @property
    def file_line_number(self):
        return self.reader.line_num

    @classmethod
    def from_file(cls, path, encoding, dialect, fields, converters):
        """Read delimited text from a text file."""

        return cls(open(path, 'r', encoding=encoding), dialect, fields, converters)

    @classmethod
    def from_zipfile(cls, path, filename, encoding, dialect, fields, converters):
        """Read delimited text from zipfile."""

        stream = ZipReader(path, filename).readlines(encoding)
        return cls(stream, dialect, fields, converters)


class DelimitedSubsetReader(DelimitedReader):
    """Read delimited text into namedtuple Records ignoring certain fields."""

    def __init__(self, stream, dialect: csv.Dialect, fields: list,
                 converters: list, field_index: list):
        super().__init__(stream, dialect, fields, converters)

        self.indexer = create_indexer(field_index)

    def __next__(self):
        indexer = self.indexer
        Record = self.Record

        row = indexer(next(self.reader))
        record = Record._make(type_converter(item) for type_converter, item
                              in zip(self.converters, row))

        return record

    @classmethod
    def from_file(cls, path, encoding, dialect, fields, converters, field_index):
        """Read delimited text from a text file."""

        return cls(open(path, 'r', encoding=encoding), dialect, fields, converters, field_index)

    @classmethod
    def from_zipfile(cls, path, filename, encoding, dialect, fields,
                     converters, field_index):
        """Read delimited text from zipfile."""

        stream = ZipReader(path, filename).readlines(encoding)
        return cls(stream, dialect, fields, converters, field_index)


class ZipReader:
    """Reads zip file.

    Parameters
    ----------
    path : Absolute path to zip file archive.
    filename : File name in archive to read.
    """

    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename

    def read(self, encoding):
        """Read content into encoded str."""
        return self.read_bytes().decode(encoding)

    def read_bytes(self):
        """Read content into byte string."""

        with ZipFile(self.path, mode='r') as archive:
            return archive.read(self.filename)

    def readlines(self, encoding):
        """Read content into encoded str line generator."""

        return (line.decode(encoding) for line in self.readlines_bytes())

    def readlines_bytes(self):
        """Read content into byte str line iterator."""

        with open_zipfile_archive(self.path, self.filename) as file:
            for line in file:
                yield line.rstrip(b'\r\n')


@contextmanager
def open_zipfile_archive(path, filename):
    with ZipFile(path, mode='r') as archive:
        with BufferedReader(archive.open(filename, mode='r')) as file:
            yield file


def concatenate_streams(streams):
    """Chain a sequence of iterators into a single stream."""

    for stream in streams:
        yield from stream
