# coding: utf-8

from unittest import TestCase


class TestIncrementField(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.fields.increment import IncrementField as Field
        return Field(*args, **kwargs)

    def test_normal_increment_field(self):
        field = self._get_class(3, 5)
        self.assertEqual(
            [field() for i in range(10)],
            [i for i in range(3, 50, 5)]
        )

    def test_datetime_increment_field(self):
        from datetime import datetime, timedelta

        def strptime(dt):
            return dt.strftime('%Y-%m-%dT%H:%M:%S')

        field = self._get_class(
            datetime(2000, 1, 1),
            timedelta(days=2, hours=8),
            strptime
        )

        self.assertEqual(
            [field() for i in range(5)],
            [
                '2000-01-01T00:00:00',
                '2000-01-03T08:00:00',
                '2000-01-05T16:00:00',
                '2000-01-08T00:00:00',
                '2000-01-10T08:00:00',
            ]
        )
