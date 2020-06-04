# coding: utf-8
from unittest import TestCase


class TestListContainer(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.containers.list import ListContainer
        return ListContainer(*args, **kwargs)

    def test_render_element_is_function(self):
        def test_function(value, i):
            return [value] * i

        lc = self._get_class(test_function)
        lc(['a', 'b', 'c'])
        self.assertEqual(
            lc,
            [
                [],
                ['b'],
                ['c', 'c'],
            ]
        )

    def test_render_normal_element(self):
        from datafactory.models.dict import DictModel

        dm = DictModel({'a': 1, 'b': 2})
        lc = self._get_class(dm)
        lc(3)
        self.assertEqual(
            lc,
            [
                {'a': 1, 'b': 2},
                {'a': 1, 'b': 2},
                {'a': 1, 'b': 2},
            ]
        )

        self.assertEqual(lc.length, 3)
