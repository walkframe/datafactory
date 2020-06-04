# coding: utf-8
import json
from datetime import time
from unittest import TestCase


class TestJsonFormatter(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.formatters.json import JsonFormatter
        return JsonFormatter(*args, **kwargs)

    def test_stringify(self):
        sf = self._get_class({'a': time(23, 59), 'b': ('2',)}, indent=None)
        self.assertEqual(
            json.loads(sf.stringify()),
            {"a": "23:59:00", "b": ["2"]}
        )

        sf = self._get_class({list}, indent=None)
        self.assertEqual(
            sf.stringify(),
            str([str(list)])
        )
