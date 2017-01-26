import ftplib
import os
import shutil
import urllib
import urllib.request
from collections import deque, defaultdict
from enum import Enum
from ftplib import FTP
from typing import Tuple, List, Iterable

from foil.filesys import ensure_file_directory


__all__ = ('ftp_listing_paths',)

FTP_URL_TEMPLATE = 'ftp://{user}:{password}@{host}:{port}'

DIRECTORY_FLAG = 'd'
FILE_FLAG = '-'
LINK_FLAG = 'l'


class ListingType(Enum):
    directory = DIRECTORY_FLAG
    file = FILE_FLAG
    link = LINK_FLAG
    other = ''


LISTING_FLAG_MAP = {FILE_FLAG: ListingType.file,
                    DIRECTORY_FLAG: ListingType.directory,
                    LINK_FLAG: ListingType.link}


def ftp_listing_paths(ftpconn: FTP, root: str) -> Iterable[str]:
    """Generate the full file paths from a root path."""

    for current_path, dirs, files in ftp_walk(ftpconn, root):
        yield from (os.path.join(current_path, file) for file in files)


def ftp_walk(ftpconn: FTP, rootpath=''):
    """Recursively traverse an ftp directory to discovery directory listing."""

    current_directory = rootpath

    try:
        directories, files = directory_listing(ftpconn, current_directory)
    except ftplib.error_perm:
        return

    # Yield before recursion
    yield current_directory, directories, files

    # Recurse into sub-directories
    for name in directories:
        new_path = os.path.join(current_directory, name)

        for entry in ftp_walk(ftpconn, rootpath=new_path):
            yield entry
    else:
        return


def directory_listing(conn: FTP, path: str) -> Tuple[List, List]:
    """Return the directories and files for single FTP listing."""

    entries = deque()
    conn.dir(path, entries.append)
    entries = map(parse_line, entries)
    grouped_entries = defaultdict(list)

    for key, value in entries:
        grouped_entries[key].append(value)

    directories = grouped_entries[ListingType.directory]
    files = grouped_entries[ListingType.file]

    return directories, files


def parse_line(line: str, char_index=0) -> Tuple[ListingType, str]:
    """Parse FTP directory listing into (type, filename)."""

    entry_name = str.rpartition(line, ' ')[-1]
    entry_type = LISTING_FLAG_MAP.get(line[char_index], ListingType.other)
    return entry_type, entry_name


def download_ftp_url(source_url, target_uri, buffer_size=8192):
    """Uses urllib. thread safe?"""

    ensure_file_directory(target_uri)

    with urllib.request.urlopen(source_url) as source_file:
        with open(target_uri, 'wb') as target_file:
            shutil.copyfileobj(source_file, target_file, buffer_size)
