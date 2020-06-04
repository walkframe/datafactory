# coding: utf-8
from datetime import datetime

from .base import BaseContainer, iterize
from ..api import render


class IterContainer(BaseContainer):
    """lazy evaluation type of container"""

    __type = None
    __iter = None

    def __iter__(self):
        starttime = datetime.now()
        try:
            for i, value in enumerate(self._iterable):
                args = [value, i]
                record = render.apply(self._blueprint, args, [None])
                if not self._filter or self._filter(record):
                    yield record
                self._progressing(i, starttime)
        except StopIteration:
            pass

    @property
    def length(self):
        return 0

    def __call__(self, iterable=None, iter=None):
        if iterable:
            self._iterable = iterize(iterable)
            self._setgoal(iterable)
        return self.__getiter(True)

    def __getiter(self, update=False):
        if update or not self.__iter:
            self.__iter = self.__iter__()
        return self.__iter

    def __next__(self):
        return next(self.__getiter())

    next = __next__
