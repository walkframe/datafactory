# coding: utf-8
from unittest import TestCase


class TestExample(TestCase):
    def test_custom_model(self):
        from datafactory import DictContainer

        def square(s, i):
            return s * i

        container = DictContainer(square)
        container(['a', 'b', 'c', 'd', 'e'])
        self.assertEqual(
            container,
            {
                'a': '',
                'b': 'b',
                'c': 'cc',
                'd': 'ddd',
                'e': 'eeee',
            }
        )

    def test_custom_field(self):
        from datafactory import Model, Container

        model = Model({
            'col1': (lambda r, i: i),
            'col2': (lambda r: r['col1'] + 1),
            'col3': (lambda r: r['col2'] * 2),
        }).ordering('col1', 'col2', 'col3')

        container = Container(model)
        container(3)
        self.assertEqual(container, [
            {'col1': 0, 'col2': 1, 'col3': 2},
            {'col1': 1, 'col2': 2, 'col3': 4},
            {'col1': 2, 'col2': 3, 'col3': 6}
        ])

    def test_combination(self):
        from datafactory import SequenceField, CycleField, ListModel, Container, ESCAPE

        l0 = ['a', 'b']
        l1 = ['a', 'b', 'c']
        l2 = ['a', 'b', 'c', 'd']

        model = ListModel([
            SequenceField(l0, repeat=len(l1) * len(l2), missing=ESCAPE),
            CycleField(l1, repeat=len(l2)),
            CycleField(l2),
        ])
        container = Container(model, 100)
        container()
        self.assertEqual(container, [
            ['a', 'a', 'a'],
            ['a', 'a', 'b'],
            ['a', 'a', 'c'],
            ['a', 'a', 'd'],
            ['a', 'b', 'a'],
            ['a', 'b', 'b'],
            ['a', 'b', 'c'],
            ['a', 'b', 'd'],
            ['a', 'c', 'a'],
            ['a', 'c', 'b'],
            ['a', 'c', 'c'],
            ['a', 'c', 'd'],
            ['b', 'a', 'a'],
            ['b', 'a', 'b'],
            ['b', 'a', 'c'],
            ['b', 'a', 'd'],
            ['b', 'b', 'a'],
            ['b', 'b', 'b'],
            ['b', 'b', 'c'],
            ['b', 'b', 'd'],
            ['b', 'c', 'a'],
            ['b', 'c', 'b'],
            ['b', 'c', 'c'],
            ['b', 'c', 'd'],
        ])
