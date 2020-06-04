# coding: utf-8
from unittest import TestCase


class TestIterContainer(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.containers.iter import IterContainer
        return IterContainer(*args, **kwargs)

    def test_length(self):
        ic = self._get_class('a')
        self.assertEqual(ic.length, 0)

    def test_iter(self):
        ic = self._get_class(
            iter([0, 1, 2, 3]),
            filter=lambda i: i % 2 == 0
        )
        ic(5)
        self.assertEqual(
            list(ic),
            [0, 2]
        )

    def test_next(self):
        ic = self._get_class('a', 2, progress=True)
        self.assertEqual(next(ic), 'a')
        self.assertEqual(next(ic), 'a')
        with self.assertRaises(StopIteration):
            next(ic)
