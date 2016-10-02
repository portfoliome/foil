"""Class dunder helper functions."""

__all__ = ['format_repr', 'format_repr_info']


def format_repr(obj, attributes) -> str:
    """Format an object's repr method with specific attributes."""

    attribute_repr = ', '.join(('{}={}'.format(attr, repr(getattr(obj, attr)))
                                for attr in attributes))
    return "{0}({1})".format(obj.__class__.__qualname__, attribute_repr)


def format_repr_info(obj, attributes) -> str:
    """Format an object's repr method indicating it's not for eval()."""

    return '<{}>'.format(format_repr(obj, attributes))
