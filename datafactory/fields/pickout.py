# coding: utf-8
from random import randint

from .base import BaseField
from ..api import display, special


class PickoutField(BaseField):
    """select an element randomly from the limited-choices."""

    def __init__(self, choices, missing=None, callback=None):
        """PickoutField constructor

        :param list or dict choices: elements of choices (element(key): element_count(value))
        :param * missing: return this value if choices is blank.
        :param function callback: function to be called at the end of rendering.
        :return: Choice Field instance.
        """
        if isinstance(choices, dict):
            self._choices = []
            for value, num in choices.items():
                self._choices += [value] * num
        else:
            self._choices = list(choices)
        self._missing = missing
        self._callbacks = [] if callback is None else [callback]

    def __repr__(self):
        return "<PickoutField {0}>".format(display.repr(self._choices, self._limit_repr))

    def __call__(self, *args):
        """render a element by randomly selection

        :param * args: any.
        :return: rendered element.
        """
        last_index = len(self._choices)
        if not last_index:
            if self._missing is special.ESCAPE:
                raise StopIteration
            return self._missing

        pop_index = randint(0, last_index - 1)
        element = self._choices.pop(pop_index)

        for callback in self._callbacks:
            element = callback(element)
        return element
