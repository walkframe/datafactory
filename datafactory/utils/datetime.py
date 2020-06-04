# coding: utf-8
from __future__ import absolute_import

import random
import re
from datetime import (
    date,
    time,
    datetime,
    timedelta as _timedelta,
)

from .. import compat

ZERO_DELTA = _timedelta()


def _to_datetime(obj):
    if isinstance(obj, datetime):
        return obj
    if isinstance(obj, date):
        return datetime.combine(obj, time(0))
    if isinstance(obj, compat.inttype):
        return datetime(obj, 1, 1)
    if isinstance(obj, (list, tuple)):
        return datetime(*obj)
    if isinstance(obj, dict):
        return datetime(**obj)
    if isinstance(obj, compat.basestring):
        obj = re.findall(r"[0-9]+", obj)
        return datetime(*map(int, obj))


def choice(start, end):
    """random choice between start and end.

    :param datetime start: datetime from.
    :param datetime end: datetime to.
    :return: datetime object that randomly selected
    """
    start = _to_datetime(start)
    end = _to_datetime(end)

    seconds_f = (end - start).total_seconds()
    seconds_i = int(seconds_f)

    chosen = random.randint(0, seconds_i)
    if seconds_i == chosen:
        microseconds = random.randint(0, int((seconds_f - seconds_i) * 1000000))
    else:
        microseconds = random.randint(0, 999999)

    return start + compat.timedelta(seconds=chosen, microseconds=microseconds)


def generator(start, end=None, interval=compat.timedelta(days=1), **noise):
    """datetime generator

    :param datetime start: datetime from
    :param timedelta interval: increase interval
    :param **noise: timedelta args(days, hours, minutes, seconds, microseconds)
    :return: iterator object
    """
    dt = _to_datetime(start)
    end = _to_datetime(end)
    if end:
        direction = (end - dt) >= ZERO_DELTA

    while end is None or (end - dt >= ZERO_DELTA) is direction or end == dt:
        _noise = {}
        for k, v in noise.items():
            if isinstance(v, tuple):
                _noise[k] = random.randint(*v)
            else:
                _noise[k] = random.randint(-v, v)
        yield dt + compat.timedelta(**_noise)
        dt += interval


def range(start, end, interval=compat.timedelta(days=1), callback=None, **noise):
    """create datetime list

    :param datetime start: datetime from
    :param datetiem end: datetime to
    :param timedelta interval: increase interval
    :param callable callback: callback that each element
    :param **noise: timedelta args(days, hours, minutes, seconds, microseconds)
    :return: list
    """
    assert end is not None
    start = _to_datetime(start)
    end = _to_datetime(end)

    return [v if callback is None else callback(v) for v in generator(start, end, interval, **noise)]
