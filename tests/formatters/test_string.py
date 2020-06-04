# coding: utf-8
import os
from unittest import TestCase


class TestStringFormatter(TestCase):
    filename = '/tmp/test_string_formatter_write.txt'

    def setUp(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    tearDown = setUp

    def _get_class(self, *args, **kwargs):
        from datafactory.formatters.string import StringFormatter
        return StringFormatter(*args, **kwargs)

    def test_string(self):
        sf = self._get_class({'a': 1, 'b': ('2',)})
        self.assertEqual(
            eval(sf.stringify()),
            {'a': 1, 'b': ('2',)}
        )

    def test_write(self):
        from datafactory.exceptions import OutputFileAlreadyExists
        sf1 = self._get_class([1])
        sf1.write(self.filename)

        self.assertEqual(
            open(self.filename).read(),
            sf1.stringify()
        )

        sf2 = self._get_class([2])
        with self.assertRaises(OutputFileAlreadyExists):
            sf2.write(self.filename)

        sf2.write(self.filename, rewrite=True)
        self.assertEqual(
            open(self.filename).read(),
            sf2.stringify()
        )
