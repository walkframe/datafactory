# coding: utf-8
from datetime import datetime

from .base import BaseContainer, iterize
from ..api import render


class ListContainer(BaseContainer, list):
    def __call__(self, iterable=None, callback=lambda v: v):
        """generate record to self(list container).

        :param iterable: iterable object or int.
        :return: rendered container.
        """
        starttime = datetime.now()
        self._setgoal(iterable)
        try:
            for i, value in enumerate(iterize(iterable) or self._iterable):
                args = [value, i]
                record = render.apply(self._blueprint, args, [None])
                if not self._filter or self._filter(record):
                    self.append(record)
                self._progressing(i, starttime)
        except StopIteration:
            pass
        return callback(self)

    def clear(self):
        """Remove from items from ListContainer"""
        self[:] = []
