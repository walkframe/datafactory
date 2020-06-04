# coding: utf-8
from __future__ import absolute_import

import csv

from .base import BaseFormatter
from ..exceptions import CsvFormatterFieldsTypeInvalid

from .. import compat


class CsvFormatter(BaseFormatter):
    def __init__(self, container, fields=None, header=None, **csvoption):
        self._container = container
        self._header = header
        self._csvoption = csvoption

        if isinstance(fields, (list, tuple, type(None))):
            self._fields = fields
        else:
            raise CsvFormatterFieldsTypeInvalid(CsvFormatterFieldsTypeInvalid.message)

    def _tolist(self, columns):
        if not isinstance(columns, (list, tuple, dict)):
            return [str(columns)]

        if self._fields is None:
            return columns.values() if isinstance(columns, dict) else columns

        result = []
        for index in self._fields:
            try:
                result.append(columns[index])
            except (KeyError, IndexError):
                result.append(None)
        return result

    def _writelines(self, file):
        if isinstance(self._container, dict):
            values = compat.viewvalues(self._container)
        else:
            values = self._container

        writer = csv.writer(file, **self._csvoption)
        if self._header:
            writer.writerow(self._header)

        for value in values:
            writer.writerow(self._tolist(value))

    def stringify(self):
        sio = compat.StringIO()
        self.write(sio)
        return sio.getvalue()

    def write(self, file, rewrite=False, **openoption):
        """container object write to file.

        :param str path: output file path.
        :param bool rewrite: rewrite if file path is already exists.
        :param kwargs openoption: io.open argments.
        :return: None
        """
        if not isinstance(file, compat.basestring):
            return self._writelines(file)

        self._write(file, rewrite, (lambda f: self._writelines(f)), **openoption)
