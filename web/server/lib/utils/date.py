# -*- coding: utf-8 -*-

import time
import datetime


def datetime_to_time(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    return int(time.mktime(dt.timetuple()))


def current_server_time():
    return int(time.time())


def tomorrow_server_time(days=1):
    return datetime_to_time(datetime.date.today() + datetime.timedelta(days=days))


def time_till_tomorrow():
    return tomorrow_server_time() - current_server_time()


def format_datetime_string(dt, output_format='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(output_format)


def time_to_datetime(val, output_format=None):
    if val == '':
        result = ''
    else:
        result = datetime.datetime.fromtimestamp(val)
        if output_format is not None:
            result = format_datetime_string(result, output_format)
    return result


def time_to_gmt_string(val):
    return format_datetime_string(time_to_datetime(val), u'%a, %d-%b-%Y %H:%M:%S GMT')


def datetime_string_to_datetime(val, output_format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(val, output_format)


def datetime_string_to_time(val, output_format='%Y-%m-%d %H:%M:%S'):
    try:
        result = datetime_to_time(datetime_string_to_datetime(val, output_format))
        if result < 0:
            result = 0
    except ValueError:
            result = 0
    return result


def datetime_now_as_string(output_format='%Y-%m-%d %H:%M:%S'):
    return format_datetime_string(datetime.datetime.now(), output_format)


def arguments_to_time(year, month, day=1, hour=0, minute=0, second=0):
    return datetime_to_time(datetime.datetime(year, month, day, hour, minute, second))


def get_day_start(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    return dt.replace(hour=0, minute=0, second=0)


def get_day_end(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    return dt.replace(hour=23, minute=59, second=59)


def get_last_day_of_month(dt=None):
    if dt is None:
        dt = datetime.date.today()
    year = dt.strftime('%Y')
    month = int(dt.strftime('%m')) % 12 + 1
    day = 1
    new_dt = datetime_string_to_datetime('%s-%s-%s' % (year, month, day), '%Y-%m-%d')
    return get_day_start(new_dt - datetime.timedelta(seconds=1))


def get_first_day_of_month(dt=None):
    if dt is None:
        dt = datetime.date.today()
    return datetime.date(dt.year, dt.month, 1)


def get_first_day_of_next_month(dt=None):
    if dt is None:
        dt = datetime.date.today()
    return datetime.date(dt.year, dt.month, 1) + datetime.timedelta()


def get_last_day_of_week(dt=None):
    if dt is None:
        dt = datetime.date.today()
    day_of_week = dt.weekday()
    return dt + datetime.timedelta(days=(6 - day_of_week) % 7)


def get_first_day_of_week(dt=None):
    if dt is None:
        dt = datetime.date.today()
    day_of_week = dt.weekday()
    return dt - datetime.timedelta(days=day_of_week)


def add_years(dt, years=1):
    try:
        return dt.replace(year=dt.year + years)
    except ValueError:
        return dt + (datetime.date(dt.year + years, 1, 1) - datetime.date(dt.year, 1, 1))


def calculate_age_from_time(val):
    return calculate_age_from_datetime(time_to_datetime(val))


def calculate_age_from_datetime(dt):
    today = datetime.date.today()
    years = today.year - dt.year

    try:
        birthday = datetime.date(today.year, dt.month, dt.day)
    except ValueError:
        # Raised when person was born on 29 February and the current
        # year is not a leap year.
        birthday = datetime.date(today.year, dt.month, dt.day - 1)

    if today < birthday:
        years -= 1

    return years


def day_difference(tm1, tm2):
    result = 0
    if tm1 < tm2:
        result = (tm2 - tm1) / 60 / 60 / 24
    return result


def milliseconds(value=None):
    if value is None:
        result = long(time.time() * 1000)
    elif isinstance(value, datetime.timedelta):
        result = long(value.total_seconds() * 1000)
    else:
        result = long(float(value) * 1000)
    return result


def seconds(value=None):
    if value is None:
        result = long(time.time())
    elif isinstance(value, datetime.timedelta):
        result = long(value.total_seconds())
    else:
        result = long(float(value) / 1000)
    return result


def get_utc_offset():
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    return offset / 60 / 60 * -1