# coding: utf-8
from unittest import TestCase


class TestSequenceField(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.fields.sequence import SequenceField as Field
        return Field(*args, **kwargs)

    def test_sequence_field_receive_list_choices(self):
        choices = [2, 4, 6]
        expect = map(str, choices)
        field = self._get_class(choices, missing=0, callback=str)
        for i in range(3):
            self.assertIn(field(), expect)

        self.assertEqual(field(), 0)

    def test_sequence_field_receive_dict_choices(self):
        from collections import OrderedDict
        choices = OrderedDict()
        for k, v in [('a', 1), ('b', 2), ('c', 3)]:
            choices[k] = v
        field = self._get_class(choices, missing='z')
        self.assertEqual(
            [field() for i in range(10)],
            [
                'a',
                'b', 'b',
                'c', 'c', 'c',
                'z', 'z', 'z', 'z'
            ]
        )
