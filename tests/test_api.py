# coding: utf-8
from unittest import TestCase


class TestRepr(TestCase):
    def _call(self, *args, **kwargs):
        from datafactory.api.display import repr
        return repr(*args, **kwargs)

    def test_normal(self):
        self.assertEqual(self._call([1, 2, 3], 50), '[1, 2, 3]')
        # self.assertEqual(
        #     self._call({'a': 1, 'b': 2, 'c': '3'}, 50),
        #     '{"a": 1, "c": "3", "b": 2}'
        # )

    def test_limit_over(self):
        self.assertEqual(self._call([1, 2, 3], 5), '[1...')

    def test_multi_byte(self):
        self.assertEqual(self._call(['あ', 'い'], 50), '["あ", "い"]')
        self.assertEqual(self._call([u'あ', u'い'], 50), u'["あ", "い"]')
        # self.assertEqual(self._call(['あ', u'い'], 50), '["\\u3042", "\\u3044"]')

    def test_can_not_be_encoded(self):
        from datetime import datetime
        d = datetime(2000, 1, 1, 10, 30, 50, 123)
        self.assertEqual(
            self._call([d], 50),
            "[datetime.datetime(2000, 1, 1, 10, 30, 50, 123)]"
        )
