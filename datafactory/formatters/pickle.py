# coding: utf-8
from __future__ import absolute_import

import pickle

from .base import BaseFormatter


class PickleFormatter(BaseFormatter):
    def __init__(self, container, protocol=0):
        self._container = container
        self._protocol = protocol

    def stringify(self):
        return pickle.dumps(self._container, self._protocol)
