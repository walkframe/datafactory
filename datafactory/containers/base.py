# coding: utf-8
from __future__ import print_function

from datetime import datetime

from .. import compat


def iterize(iterable):
    """convert to iterable object.

    :param iterable iterable:
    :return: iterable objects
    """
    if iterable is None:
        return None

    if isinstance(iterable, compat.inttype):
        return compat.xrange(iterable)

    return iterable


class BaseContainer(object):
    """Base Container object."""

    def __init__(self, blueprint, iterable=(), filter=None, progress=False, render=False):
        """BaseContainer constructor

        :param * blueprint: field / model / container / function / else (fixed value)
        :param iterable or int iterable: repeat info.
        :return: container instance.
        """
        self._blueprint = blueprint
        self._iterable = iterize(iterable)
        self._filter = filter
        self._progress = progress
        self._setgoal(iterable)
        if render:
            self(iterable)

    @property
    def length(self):
        return len(self)

    def _setgoal(self, iterable):
        if isinstance(iterable, compat.inttype):
            self._goal = iterable
        elif hasattr(iterable, "__len__"):
            self._goal = iterable.__len__()
        elif not hasattr(self, "_goal"):
            self._goal = None

    def _progressing(self, current, starttime):
        if not self._progress:
            return
        current += 1
        message = "[{0}] {1}/{2}".format(str(datetime.now() - starttime).split(".")[0], current, self._goal or "?")
        if self._goal:
            message += " ({0:03.1f}%)".format(current / float(self._goal or 1) * 100)
        print(message + "\r", end="")

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()
