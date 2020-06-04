# coding: utf-8
from __future__ import absolute_import

from .base import BaseFormatter


class StringFormatter(BaseFormatter):
    def __init__(self, container):
        self._container = container

    def stringify(self):
        return str(self._container)
