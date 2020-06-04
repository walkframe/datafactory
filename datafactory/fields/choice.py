# coding: utf-8
from random import choice

from .base import BaseField
from ..api import display


class ChoiceField(BaseField):
    """select an element randomly from the choices."""

    def __init__(self, choices, callback=None):
        """ChoiceField constructor

        :param choices: list-elements of choices
        :param callback: function to be called at the end of rendering.
        :return: Choice Field instance.
        """
        if isinstance(choices, dict):
            self._choices = []
            for value, num in choices.items():
                self._choices += [value] * num
        else:
            self._choices = choices
        self._callbacks = [] if callback is None else [callback]

    def __repr__(self):
        return "<ChoiceField {0}>".format(display.repr(self._choices, self._limit_repr))

    def __call__(self, *args):
        """render a element by randomly selection

        :param args: any.
        :return: rendered element.
        """
        element = choice(self._choices)
        for callback in self._callbacks:
            element = callback(element)
        return element
