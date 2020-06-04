# coding: utf-8
import os
from unittest import TestCase


class TestCsvFormatter(TestCase):
    filename = '/tmp/test_csv_formatter_write.txt'

    def setUp(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    tearDown = setUp

    def _get_class(self, *args, **kwargs):
        from datafactory.formatters.csv import CsvFormatter
        return CsvFormatter(*args, **kwargs)

    def test_stringify_list_fields_csv(self):
        sf = self._get_class([
            (1, 2, 3),
            (4, 5, 6),
        ])
        self.assertEqual(
            sf.stringify(),
            (
                "1,2,3\r\n"
                "4,5,6\r\n"
            )
        )

    def test_stringify_dict_fields_tsv(self):
        sf = self._get_class([
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 4, 'b': 5, 'c': 6},
        ], fields=['a', 'b', 'c'], delimiter='\t', lineterminator='\n')
        self.assertEqual(
            sf.stringify(),
            (
                "1\t2\t3\n"
                "4\t5\t6\n"
            )
        )

    def test_write_list_fields_tsv(self):
        from datafactory.exceptions import OutputFileAlreadyExists

        sf = self._get_class(
            [
                {'a': 1, 'b': 2, 'c': 3},
                {'a': 4, 'b': 5, 'c': 6},
            ],
            fields=['a', 'b', 'c'],
            header=['a', 'b', 'c'],
            delimiter='\t',
            lineterminator='\n'
        )

        sf.write(self.filename)
        self.assertEqual(
            open(self.filename).read(),
            (
                "a\tb\tc\n"
                "1\t2\t3\n"
                "4\t5\t6\n"
            )
        )

        with self.assertRaises(OutputFileAlreadyExists):
            sf.write(self.filename)
