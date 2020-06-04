# coding: utf-8

from unittest import TestCase


def gen_value(element, seq_num, seq_key):
    return str(element[1]) + ' + ' + (str(seq_key) * seq_num)


class TestListModel(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.models.list import ListModel
        return ListModel(*args, **kwargs)

    def test_order(self):
        le = self._get_class(['a', 'b', 'c', 'd'])
        le.ordering(3, 2)
        self.assertEqual(le._order, [3, 2, 0, 1])

    def test_order_negative_index(self):
        le = self._get_class(['a', 'b', 'c', 'd'])
        le.ordering(-4, -1)
        self.assertEqual(le._order, [0, 3, 1, 2])

    def test_render(self):
        from datafactory.fields.increment import IncrementField

        le = self._get_class([
            gen_value,
            IncrementField(),
            3
        ]).ordering(1)

        self.assertEqual(
            [
                le(i, key)
                for i, key in enumerate(['a', 'b', 'c'])
            ],
            [
                ['1 + ', 1, 3],
                ['2 + b', 2, 3],
                ['3 + cc', 3, 3]
            ],
        )

    def test_render_nesting(self):
        lm = self._get_class([
            1,
            self._get_class([2, 3])
        ])

        self.assertEqual(
            [
                lm(i, key)
                for i, key in enumerate(range(3))
            ],
            [[1, [2, 3]]] * 3
        )

    def test_custom_render(self):
        from datafactory.fields.increment import IncrementField

        lm = self._get_class([
            (lambda record: str(record[1])),
            IncrementField()
        ]).ordering(1)

        self.assertEqual(
            [
                lm(i, key)
                for i, key in enumerate(range(3))
            ],
            [['1', 1], ['2', 2], ['3', 3]]

        )

    def test_render_blank(self):
        from datafactory.fields.cycle import CycleField
        from datafactory.api.special import BLANK

        lm = self._get_class([
            0,
            BLANK,
            CycleField([1, BLANK, 3])
        ])

        self.assertEqual(
            [
                lm(i, key)
                for i, key in enumerate(range(10))
            ],
            [
                [0, 1], [0], [0, 3],
                [0, 1], [0], [0, 3],
                [0, 1], [0], [0, 3],
                [0, 1],
            ]
        )
