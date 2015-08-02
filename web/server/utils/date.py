# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2012-12-27'

import time
import datetime
import logging

from settings import TIME_ZONE_OFFSET, TIME_ZONE_GMT_OFFSET

logger = logging.getLogger('default')


def current_server_time():
    return int(time.mktime(datetime.datetime.now().timetuple())) + TIME_ZONE_OFFSET


def tomorrow_server_time(days=1):
    return int(time.mktime((datetime.date.today() + datetime.timedelta(days=days)).timetuple())) + TIME_ZONE_OFFSET


def time_till_tomorrow():
    return tomorrow_server_time() - current_server_time()


# %Y-%m-%d %H:%M:%S
def time_to_datetime(val, output_format=None):
    if val == '':
        return ''

    new_val = datetime.datetime.fromtimestamp(val - TIME_ZONE_OFFSET)
    if output_format is not None:
        return new_val.strftime(output_format)

    return new_val


def time_to_gmt_string(val):
    return (time_to_datetime(val + TIME_ZONE_GMT_OFFSET)).strftime(u'%a, %d-%b-%Y %H:%M:%S GMT')


def datetime_string_to_datetime(val, output_format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(val, output_format)


def datetime_string_to_time(val, output_format='%Y-%m-%d %H:%M:%S'):
    val = int(time.mktime(datetime_string_to_datetime(val, output_format).timetuple()) + TIME_ZONE_OFFSET)
    if val < 0:
        return 0
    return val


def datetime_now_as_string(output_format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(output_format)


def calculate_age_from_time(val):
    return calculate_age_from_datetime(time_to_datetime(val))


def calculate_age_from_datetime(datetime_obj):
    today = datetime.date.today()
    years = today.year - datetime_obj.year

    try:
        birthday = datetime.date(today.year, datetime_obj.month, datetime_obj.day)
    except ValueError:
        # Raised when person was born on 29 February and the current
        # year is not a leap year.
        birthday = datetime.date(today.year, datetime_obj.month, datetime_obj.day - 1)

    if today < birthday:
        years -= 1

    return years


def day_difference(tm1, tm2):
    if tm1 < tm2:
        return (tm2 - tm1) / 60 / 60 / 24
    return 0


def milliseconds(value=None):
    if value is None:
        return long(time.time() * 1000)
    elif isinstance(value, datetime.timedelta):
        return long(value.total_seconds() * 1000)
    else:
        return long(float(value) * 1000)


def seconds(value=None):
    if value is None:
        return long(time.time())
    elif isinstance(value, datetime.timedelta):
        return long(value.total_seconds())
    else:
        return long(float(value) / 1000)