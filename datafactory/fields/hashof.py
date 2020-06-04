# coding: utf-8
import hashlib

from .base import BaseField
from ..api import display
from .. import compat


class HashOfField(BaseField):
    """generate hash value."""

    def __init__(self, subscript, method="md5", stringify=compat.stringify, callback=None):
        """HashOfField constructor

        :param immutable-obj subscript: record subscript.
        :param str method: hash method type.(md5 / sha1 / sha224 / sha256 / sha384 / sha512)
        :param function stringify: stringify function to give hash method.
        :param function callback: function to be called at the end of rendering.
        :return: Hash Field instance.
        """
        self._subscript = subscript
        self._method = method
        self._hash = getattr(hashlib, method.lower())
        self._stringify = stringify
        self._callbacks = [] if callback is None else [callback]

    def __repr__(self):
        info = "{0} of record[{1}]".format(self._method.upper(), self._subscript)
        return "<HashField {0}>".format(display.ellipsis(info, self._limit_repr))

    def __call__(self, record, *args):
        """render a element by hash method.

        :param record: record to be written by field().
        :param * args: any
        :return: rendered element.
        """
        seed = record[self._subscript]

        element = self._hash(self._stringify(seed)).hexdigest()
        for callback in self._callbacks:
            element = callback(element)
        return element
