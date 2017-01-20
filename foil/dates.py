import datetime as dt
import re
from types import MappingProxyType

import pytz

from foil.compose import cartesian_product


class IsoDatePattern:
    """Builds ISO 8601 date and time regular expression patterns.

    The format follows:
    YYYY[dsep]MM[dsep]DD[dtsep]HH[tsep]MM[tsep]SS[.ffffff][tzsep]TZ,

    Example str to match:
    '2014-02-14T11:12:04.343 EST'
    """

    YEAR = r'(?P<year>\d{4})'
    MONTH = r'(?P<month>[0-1]\d)'
    DAY = r'(?P<day>[0-3]\d)'
    HOUR = r'(?P<hour>2[0-3]|[0-1]\d|\d)'
    MINUTE = r'(?P<minute>[0-5]\d)'
    SECOND = r'(?P<second>[0-5]\d)'
    MICROSECOND = r'(.?(?P<microsecond>\d{3,6})?)'
    TIMEZONE = r'(?P<timezone>[A-Z][A-Z_]+(?:/[A-Z][A-Z_]+)+|[A-Z]{3,})?'

    def __init__(self, dsep=r'-', tsep=r':', dtsep=r'[T|\s]?', tzsep=r'\s?'):
        self.date = _format_re(dsep.join([self.YEAR, self.MONTH, self.DAY]))
        self.time = _format_re(tsep.join([self.HOUR, self.MINUTE, self.SECOND]) + self.MICROSECOND)
        self.datetime = dtsep.join([self.date, self.time])
        self.datetimezone = tzsep.join([self.datetime, self.TIMEZONE])


def _format_re(pattern):
    return r'(?:{})?'.format(pattern)


_RE_DATE = re.compile(r'^{}$'.format(IsoDatePattern().date))
_RE_DATETIMEZONE = re.compile(IsoDatePattern().datetimezone)

TIMEZONE_MAP = MappingProxyType(dict(cartesian_product(
    (('EST', 'EDT', 'EST/EDT'), pytz.timezone('US/Eastern')))))


def parse_date(date_str: str, pattern=_RE_DATE) -> dt.date:
    """Parse datetime.date from YYYY-MM-DD format."""

    groups = re.match(pattern, date_str)

    return dt.date(*_date_to_tuple(groups.groupdict()))


class DateTimeParser:

    def __init__(self, pattern=_RE_DATETIMEZONE, tz_mapper=TIMEZONE_MAP):
        self.pattern = pattern
        self.tz_mapper = tz_mapper

    def parse(self, date_str) -> dt.datetime:
        gd = self.pattern.match(date_str).groupdict()

        if gd['microsecond'] is not None:
            gd['microsecond'] = (gd['microsecond'] + '000000')[:6]

        datetime_ = dt.datetime(*_datetime_to_tuple(gd))

        if gd.get('timezone') is not None:
            datetime_ = self.convert_2_utc(datetime_, gd.get('timezone'))

        return datetime_

    def convert_2_utc(self, datetime_, timezone):
        """convert to datetime to UTC offset."""

        datetime_ = self.tz_mapper[timezone].localize(datetime_)
        return datetime_.astimezone(pytz.UTC)


def _datetime_to_tuple(dt_dict):
    """datetime.datetime components from dictionary to tuple.

    Example
    -------
    dt_dict = {'year': '2014','month': '07','day': '23',
            'hour': '13','minute': '12','second': '45','microsecond': '321'}

    _datetime_to_tuple(dt_dict) -> (2014, 7, 23, 13, 12, 45, 321)
    """

    year, month, day = _date_to_tuple(dt_dict)
    hour, minute, second, microsecond = _time_to_tuple(dt_dict)

    return year, month, day, hour, minute, second, microsecond


def _date_to_tuple(dt_dict):

    ymd = ['year', 'month', 'day']

    try:
        year, month, day = [int(dt_dict[d]) for d in ymd]
    except TypeError:
        raise TypeError('date components must cast to ints.')

    return year, month, day


def _time_to_tuple(dt_dict):

    times = ['hour', 'minute', 'second', 'microsecond']

    hour, minute, second, microsecond = (
        int(dt_dict[t]) if dt_dict[t] is not None else 0 for t in times)

    return hour, minute, second, microsecond
