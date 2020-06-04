# coding: utf-8
from .base import BaseField
from ..api import display


class CycleField(BaseField):
    """select an element regularly from the sequence."""

    def __init__(self, sequence, increment=1, repeat=1, callback=None):
        """CycleField constructor

        :param list or dict sequence: elements of sequence (element(key): element_count(value))
        :param int increment: list-index increase.
        :param int repeat: intervals up proceeds to the next element.
        :param function callback: function to be called at the end of rendering.
        :return: Cycle Field instance.
        """
        assert repeat > 0
        if isinstance(sequence, dict):
            self._sequence = []
            for value, num in sequence.items():
                self._sequence += [value] * num
        else:
            self._sequence = sequence
        self._size = len(self._sequence)
        self._index = 0
        self._total = 0
        self._repeat = repeat
        self._increment = increment
        self._callbacks = [] if callback is None else [callback]

    def __repr__(self):
        return "<CycleField {0}>".format(display.repr(self._sequence, self._limit_repr))

    def __call__(self, *args):
        """render a element by regularly selection.

        :param args: any.
        :return: rendered element.
        """
        element = self._sequence[self._index % self._size]

        self._total += 1
        if self._total % self._repeat == 0:
            self._index += self._increment
        for callback in self._callbacks:
            element = callback(element)
        return element
