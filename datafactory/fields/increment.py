# coding
from .base import BaseField
from ..api.display import ellipsis


class IncrementField(BaseField):
    """generate element by addition of value that regular."""

    def __init__(self, start=1, step=1, callback=None):
        """IncrementField constructor

        :param * start: initial value.
        :param * step: increase. (computable type with start)
        :param function callback: function to be called at the end of rendering.
        :return: Increment Field instance
        """
        self._element = start
        self._step = step
        self._callbacks = [] if callback is None else [callback]

    def __repr__(self):
        info = "{0}::{1}".format(self._element, self._step)
        return "<IncField {0}>".format(ellipsis(info, self._limit_repr))

    def __call__(self, *args):
        """render a element by regularly addition.

        :param * args: any.
        :return: rendered element.
        """
        element = self._element
        self._element += self._step
        for callback in self._callbacks:
            element = callback(element)
        return element
