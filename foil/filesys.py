"""File system operations."""

import os


def file_exists(file_path):
    """Check if the full file path exists."""

    try:
        with open(file_path, 'r'):
            return True
    except IOError:
        raise FileExistsError


def ensure_directory(path: str):
    """Ensure that a directory path exists."""

    try:
        os.makedirs(path, exist_ok=False)
    except FileExistsError:
        pass


def ensure_file_directory(file_path: str):
    """Ensure that a directory path exists."""

    ensure_directory(os.path.dirname(file_path))
