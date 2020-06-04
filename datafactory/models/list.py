# coding: utf-8
from .base import BaseModel
from ..api import render, special


class ListModel(BaseModel, list):
    """list-structure that is repeatedly drawn."""

    __type = list

    def __init__(self, params, callback=None):
        """define list-structure model.

        :param list params: elements.
        :return: ListModel instance.
        """
        self += params

        self._length = len(self)
        self._order = range(self._length)
        self._callback = callback

    def ordering(self, *order):
        """order in which list-index to generate the elements.

        :param int order: order of subscripts. (variable-length argument)
        :return: self(model).
        """
        self._order = []
        for subscript in order:
            if subscript < 0:
                subscript += self._length
            self._order.append(subscript)

        for subscript in range(self._length):
            if subscript not in self._order:
                self._order.append(subscript)
        return self

    def __call__(self, key, index):
        """rendering a list-structure record.

        :param int index: index of iterable-object to render container object.
        :param immutable-obj key: element of iterable-object to render container object.
        :return: rendered record.
        """
        record = [None] * self._length
        del_indexes = []
        for subscript in self._order:
            blueprint = self[subscript]
            args = [record, key, index]
            value = render.apply(blueprint, args)
            if value is special.BLANK:
                del_indexes.append(subscript)
            else:
                record[subscript] = value

        for index in sorted(del_indexes, reverse=True):
            del record[index]

        if self._callback:
            record = self._callback(record)

        return record
