# coding: utf-8
from unittest import TestCase


def gen_value(element, seq_num, seq_key):
    return str(element['b']) + ' + ' + (str(seq_key) * seq_num)


class TestDictModel(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.models.dict import DictModel
        return DictModel(*args, **kwargs)

    def test_order(self):
        dm = self._get_class({
            'a': 1, 'b': 2, 'c': 3, 'd': 4,
        })
        dm.ordering('d', 'b', 'c')
        self.assertEqual(dm._order, ['d', 'b', 'c', 'a'])

    def test_render(self):
        from datafactory.fields.increment import IncrementField

        dm = self._get_class({
            'a': gen_value,
            'b': IncrementField(),
            'c': 3
        }).ordering('b')

        self.assertEqual(
            [
                dm(i, key)
                for i, key in enumerate(['a', 'b', 'c'])
            ],
            [
                {'a': '1 + ', 'b': 1, 'c': 3},
                {'a': '2 + b', 'b': 2, 'c': 3},
                {'a': '3 + cc', 'b': 3, 'c': 3},
            ],
        )

    def test_render_nesting(self):
        dm = self._get_class({
            'a': 1,
            'b': self._get_class({'c': 1})
        })

        self.assertEqual(
            [
                dm(i, key)
                for i, key in enumerate(range(3))
            ],
            [{'a': 1, 'b': {'c': 1}}] * 3
        )

    def test_custom_render(self):
        from datafactory.fields.increment import IncrementField

        dm = self._get_class({
            'a': (lambda record: str(record['b'])),
            'b': IncrementField()
        }).ordering('b', 'a')

        self.assertEqual(
            [
                dm(i, key)
                for i, key in enumerate(range(3))
            ],
            [
                {'a': '1', 'b': 1},
                {'a': '2', 'b': 2},
                {'a': '3', 'b': 3},
            ]
        )

    def test_render_blank(self):
        from datafactory.fields.cycle import CycleField
        from datafactory.api.special import BLANK

        dm = self._get_class({
            'a': BLANK,
            'b': CycleField([1, BLANK, 3])
        })

        self.assertEqual(
            [
                dm(i, key)
                for i, key in enumerate(range(10))
            ],
            [
                {'b': 1}, {}, {'b': 3},
                {'b': 1}, {}, {'b': 3},
                {'b': 1}, {}, {'b': 3},
                {'b': 1},
            ]
        )
