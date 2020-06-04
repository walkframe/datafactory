# coding: utf-8
from unittest import TestCase


class TestIterize(TestCase):
    def _call(self, *args, **kwargs):
        from datafactory.containers.base import iterize
        return iterize(*args, **kwargs)

    def test_none(self):
        self.assertIsNone(
            self._call(None)
        )

    def test_int(self):
        i = 3
        self.assertEqual(
            [j for j in self._call(i)],
            [j for j in range(i)]
        )


class TestBaseContainer(TestCase):
    def test_repeat(self):
        from datafactory.containers.base import BaseContainer
        bc = BaseContainer(None, 'abc')
        self.assertEqual(bc._iterable, 'abc')
