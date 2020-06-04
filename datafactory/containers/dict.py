# coding: utf-8
from datetime import datetime

from .base import BaseContainer, iterize
from ..api import render


class DictContainer(BaseContainer, dict):
    def __call__(self, iterable=None, callback=lambda v: v):
        """generate record to self(dict container).

        :param iterable or int iterable: element of in iterable become key.
        :return: rendered container.
        """
        starttime = datetime.now()
        self._setgoal(iterable)
        try:
            for i, value in enumerate(iterize(iterable) or self._iterable):
                args = [value, i]
                record = render.apply(self._blueprint, args, [None])
                if not self._filter or self._filter(record):
                    self[value] = record
                self._progressing(i, starttime)
        except StopIteration:
            pass
        return callback(self)
