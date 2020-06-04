# coding: utf-8
from __future__ import absolute_import

import json
from datetime import datetime, date, time

from .base import BaseFormatter


class JSONEncoder(json.JSONEncoder):
    """Custom JSON Encoder for Container"""

    ENCODERS = {
        datetime: (lambda dt: dt.isoformat()),
        date: (lambda d: d.isoformat()),
        time: (lambda t: t.isoformat()),
        set: list,
    }

    def default(self, o):
        try:
            encoder = self.ENCODERS[type(o)]
            return encoder(o)
        except KeyError:
            return str(o)


class JsonFormatter(BaseFormatter):
    def __init__(self, container, **jsonoption):
        self._container = container
        jsonoption.setdefault("indent", 1)
        jsonoption.setdefault("cls", JSONEncoder)
        self._jsonoption = jsonoption

    def stringify(self):
        return json.dumps(self._container, **self._jsonoption)
