import re


CAMEL_CASE_RE = re.compile(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')


def camel_to_snake(s: str) -> str:
    """Convert string from camel case to snake case."""

    return CAMEL_CASE_RE.sub(r'_\1', s).strip().lower()


def snake_to_camel(s: str) -> str:
    """Convert string from snake case to camel case."""

    fragments = s.split('_')

    return fragments[0] + ''.join(x.title() for x in fragments[1:])
