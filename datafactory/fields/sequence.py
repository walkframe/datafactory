# coding: utf-8
from .base import BaseField
from ..api import display, special


class SequenceField(BaseField):
    """select an element sequentially."""

    def __init__(self, sequence, missing=None, repeat=1, callback=None):
        """SequenceField constructor

        :param list or dict sequence: elements of sequence (element(key): element_count(value))
        :param * missing: return this value if reached last element.
        :param int repeat: intervals up proceeds to the next element.
        :param function callback: function to be called at the end of rendering.
        :return: Choice Field instance.
        """
        assert repeat > 0
        if isinstance(sequence, dict):
            self._sequence = []
            for value, num in sequence.items():
                self._sequence += [value] * num
        else:
            self._sequence = sequence
        self._size = len(self._sequence) - 1
        self._missing = missing
        self._index = 0
        self._total = 0
        self._repeat = repeat
        self._callbacks = [] if callback is None else [callback]

    def __repr__(self):
        return "<SeqField {0}>".format(display.repr(self._sequence, self._limit_repr))

    def __call__(self, *args):
        """render a element

        :param * args: any.
        :return: rendered element.
        """
        if self._index > self._size:
            if self._missing is special.ESCAPE:
                raise StopIteration
            return self._missing

        element = self._sequence[self._index]
        self._total += 1
        if self._total % self._repeat == 0:
            self._index += 1

        for callback in self._callbacks:
            element = callback(element)
        return element
