import os
import re
from hashlib import sha256
from typing import Iterable, Pattern
from zipfile import ZipFile

from foil.util import alphanum_key


def find_latest_file(top: str, pattern: Pattern) -> str:
    """Find latest file matching a pattern in each directory.

    Find latest file defined by a file pattern and natural sort
    for each directory and sub directory a file pattern match
    occurs.

    Parameters
    ----------
    top : base directory path
    pattern : regular expression to match file name pattern

    Yields
    ------
    full file paths matching pattern.

    """

    for root, dirs, files in os.walk(top):
        try:
            file_name = max(match_files(files, pattern), key=alphanum_key)

            yield os.path.join(root, file_name)
        except ValueError:
            pass


def match_file_listing(paths, pattern: Pattern):
    for path in paths:
        filename = os.path.basename(path)

        if re.match(pattern, filename):
            yield path


def match_files(files, pattern: Pattern):
    """Yields file name if matches a regular expression pattern."""

    for name in files:
        if re.match(pattern, name):
            yield name


def match_zipfile_members(zipfile_path: str, pattern: Pattern):
    """Match files to a pattern within a zip file's content."""

    with ZipFile(zipfile_path, mode='r') as zfile:
        members = zfile.namelist()

    yield from match_files(members, pattern)


def find_zipfile_member(zipfile_path: str, pattern: Pattern):
    """Return the first match to a regex within a zip file's content."""

    return next(match_zipfile_members(zipfile_path, pattern))


def directory_files(path):
    """Yield directory file names."""

    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_file():
            yield entry.name


def get_file_listing_sha(listing_paths: Iterable) -> str:
    """Return sha256 string for group of FTP listings."""

    return sha256(''.join(sorted(listing_paths)).encode('utf-8')).hexdigest()


def merge_paths(base_path, path):
    """Merge a base path with another full path, path."""

    return os.path.join(base_path, strip_full_path(path))


def strip_full_path(path):
    """String away a path separator prefix."""

    relative_path = path.lstrip(os.sep)
    return relative_path


def strip_file_listing(paths):
    """Remove the file listing(s) from the directory path(s)."""

    return (os.path.split(path)[0] for path in paths)


def unique_listing_directories(file_listing) -> set:
    """Return unique directory set for file listing collection."""

    directories = strip_file_listing(file_listing)
    return set(directories)
