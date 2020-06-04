# coding: utf-8
from unittest import TestCase


class TestPickoutField(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.fields.pickout import PickoutField as Field
        return Field(*args, **kwargs)

    def test_pickout_field_receive_list_choices(self):
        choices = [2, 4, 6]
        expect = [i for i in map(str, choices)]
        field = self._get_class(choices, missing=0, callback=str)
        for i in range(3):
            self.assertIn(field(), expect)

        self.assertEqual(field(), 0)

    def test_pickout_field_receive_dict_choices(self):
        choices = {'a': 1, 'b': 2, 'c': 3}
        field = self._get_class(choices)
        expect = ['a', 'b', 'c']
        for i in range(6):
            self.assertIn(field(), expect)

        self.assertIsNone(field())
