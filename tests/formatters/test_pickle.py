# coding: utf-8
import os
import pickle
from unittest import TestCase


class TestPickleFormatter(TestCase):
    filename = '/tmp/test_json_formatter_write.txt'

    def setUp(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    tearDown = setUp

    def _get_class(self, *args, **kwargs):
        from datafactory.formatters.pickle import PickleFormatter
        return PickleFormatter(*args, **kwargs)

    def test_stringify(self):
        sf = self._get_class({'a': 1, 'b': ('2',)}, protocol=2)
        self.assertEqual(
            sf.stringify(),
            pickle.dumps({'a': 1, 'b': ('2',)}, protocol=2)
        )
