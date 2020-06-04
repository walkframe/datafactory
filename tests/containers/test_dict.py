# coding: utf-8
from unittest import TestCase


class TestDictContainer(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.containers.dict import DictContainer
        return DictContainer(*args, **kwargs)

    def test_render_element_is_function(self):
        def test_function(value, i):
            return [value] * i

        dc = self._get_class(test_function)
        dc(['a', 'b', 'c'])
        self.assertEqual(
            dc,
            {
                'a': [],
                'b': ['b'],
                'c': ['c', 'c'],
            }
        )

    def test_render_normal_element(self):
        from datafactory.models.list import ListModel

        lm = ListModel([1, 2])
        dc = self._get_class(lm)
        dc(['a', 'b', 'c'])
        self.assertEqual(
            dc,
            {
                'a': [1, 2],
                'b': [1, 2],
                'c': [1, 2],
            }
        )

    def test_missing_escape(self):
        from datafactory.fields.sequence import SequenceField
        from datafactory.api.special import ESCAPE

        dc = self._get_class(
            SequenceField([0, 1, 2, 3], missing=ESCAPE)
        )
        dc('abcdefg')
        self.assertEqual(
            dc,
            {
                'a': 0,
                'b': 1,
                'c': 2,
                'd': 3,
            }
        )
