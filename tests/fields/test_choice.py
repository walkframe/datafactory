# coding: utf-8
from unittest import TestCase


class TestChoiceField(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.fields.choice import ChoiceField as Field
        return Field(*args, **kwargs)

    def test_choice_field_receive_list_choices(self):
        choices = [2, 4, 6]
        expect = [i for i in map(str, choices)]
        field = self._get_class(choices, str)
        for i in range(100):
            self.assertIn(field(), expect)

    def test_choice_field_dict_choices(self):
        choices = {'a': 1, 'b': 2, 'c': 3}
        expect = choices.keys()
        field = self._get_class(choices, str)
        for i in range(100):
            self.assertIn(field(), expect)
