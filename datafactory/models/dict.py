# coding: utf-8
from .base import BaseModel
from ..api import render, special


class DictModel(BaseModel, dict):
    """dict structure that is repeatedly drawn."""

    __type = dict

    def __init__(self, params, callback=None):
        """define dict-structure model.

        :param dict params: elements.
        :return: DictModel instance.
        """
        self.update(params)

        self._length = len(self)
        self._order = self.keys()
        self._callback = callback

    def ordering(self, *order):
        """order in which list-index to generate the elements.

        :param immutable-obj order: order of subscripts. (variable-length argument)
        :return: self(model).
        """
        self._order = list(order)
        for subscript in self.keys():
            if subscript not in self._order:
                self._order.append(subscript)
        return self

    def __call__(self, key, index):
        """rendering a dict-structure record.

        :param int index: index of iterable-object to render container object.
        :param immutable-obj key: element of iterable-object to render container object.
        :return: rendered record.
        """
        record = self.__type()
        for subscript in self._order:
            blueprint = self[subscript]
            args = [record, key, index]
            value = render.apply(blueprint, args)
            subscript = render.apply(subscript, args)
            if not (value is special.BLANK or subscript is special.BLANK):
                record[subscript] = value

        if self._callback:
            record = self._callback(record)

        return record
