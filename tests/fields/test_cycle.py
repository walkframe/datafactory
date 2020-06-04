# coding: utf-8
from unittest import TestCase


class TestCycleField(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.fields.cycle import CycleField as Field
        return Field(*args, **kwargs)

    def test_cycle_field(self):
        field = self._get_class([1, 2, 3], callback=str)
        self.assertEqual(
            [field() for i in range(5)],
            ['1', '2', '3', '1', '2']
        )

    def test_cycle_field_receive_dict_choices(self):
        from collections import OrderedDict
        choices = OrderedDict()
        for k, v in [('a', 1), ('b', 2), ('c', 3)]:
            choices[k] = v
        field = self._get_class(choices)
        self.assertEqual(
            [field() for i in range(10)],
            [
                'a',
                'b', 'b',
                'c', 'c', 'c',
                'a',
                'b', 'b',
                'c',
            ]
        )
