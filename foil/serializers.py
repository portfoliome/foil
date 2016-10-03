import json
import uuid
from datetime import date, datetime
from functools import singledispatch


@singledispatch
def json_serializer(obj):
    return json.dumps(obj)


@json_serializer.register(uuid.UUID)
def _(obj):
    return str(obj)


@json_serializer.register(date)
def _(obj):
    return obj.isoformat()


@json_serializer.register(datetime)
def _(obj):
    # Interpret naive datetime as UTC with zulu suffix.
    zulu_suffix = 'Z' if obj.tzinfo is None else ''
    return obj.isoformat() + zulu_suffix
