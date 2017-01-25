import json
import uuid
from datetime import date, datetime, timedelta
from functools import singledispatch


UTC_ZERO = timedelta(0)


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
    """ISO 8601 format. Interprets naive datetime as UTC with zulu suffix."""

    tz_offset = obj.utcoffset()

    if not tz_offset or tz_offset == UTC_ZERO:
        iso_datetime = obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        iso_datetime = obj.isoformat()

    return iso_datetime
