"""File system operations."""


def file_exists(file_path):
    """Check if the full file path exists."""

    try:
        with open(file_path, 'r'):
            return True
    except IOError:
        raise FileExistsError
