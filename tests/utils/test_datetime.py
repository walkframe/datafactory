# coding: utf-8
from unittest import TestCase
from datetime import datetime, timedelta

start = datetime(2014, 10, 20)
end = datetime(2014, 10, 21, 12, 30, 30, 123456)


class TestGenerator(TestCase):
    def _call(self, *args, **kwargs):
        from datafactory.utils.datetime import generator
        return generator(*args, **kwargs)

    def test_generator(self):
        delta = timedelta(days=1, hours=12)
        g = self._call(start, interval=delta)
        for i in range(1000):
            self.assertEqual(next(g), start + (delta * i))

    def test_generator_has_end_argument(self):
        delta = timedelta(hours=12)
        g = self._call(start, end, interval=delta)
        self.assertEqual(next(g), datetime(2014, 10, 20))
        self.assertEqual(next(g), datetime(2014, 10, 20, 12))
        self.assertEqual(next(g), datetime(2014, 10, 21))
        self.assertEqual(next(g), datetime(2014, 10, 21, 12))
        with self.assertRaises(StopIteration):
            next(g)

    def test_generator_with_noise_as_int(self):
        delta = timedelta(days=1)
        noise = dict(hours=23, minutes=59, seconds=59, microseconds=999999)
        g = self._call(start, interval=delta, **noise)
        for i in range(1000):
            fact = next(g)

            max_noise = timedelta(**noise)
            from_dt = start + (delta * i) - max_noise
            to_dt = start + (delta * i) + max_noise
            self.assertTrue(from_dt <= fact <= to_dt)
            # self.assertNotEqual(start + (delta * i), fact)

    def test_generator_with_noise_as_tuple(self):
        delta = timedelta(days=1)
        noise = dict(hours=(20, 23))
        g = self._call(start, interval=delta, **noise)
        for i in range(1000):
            fact = next(g)

            min_noise = timedelta(hours=20)
            max_noise = timedelta(hours=23)

            from_dt = start + (delta * i) + min_noise
            to_dt = start + (delta * i) + max_noise
            self.assertTrue(from_dt <= fact <= to_dt)
            # self.assertNotEqual(start + (delta * i), fact)


class TestRange(TestCase):
    def _call(selfself, *args, **kwargs):
        from datafactory.utils.datetime import range
        return range(*args, **kwargs)

    def test_range_with_callback(self):
        def callback(dt):
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

        delta = timedelta(hours=1, minutes=30)
        ranges = [
            callback(start + (delta * i))
            for i in range(25)
        ]
        self.assertEqual(self._call(start, end, delta, callback=callback), ranges)


class TestChoice(TestCase):
    def _call(self, *args, **kwargs):
        from datafactory.utils.datetime import choice
        return choice(*args, **kwargs)

    def test_choice(self):
        for i in range(1000):
            self.assertTrue(start <= self._call(start, end) <= end)

    def test_choice_short_period(self):
        start2 = datetime(2000, 1, 1)
        end2 = datetime(2000, 1, 1, 0, 0, 0, 10)
        for i in range(10):
            self.assertTrue(start2 <= self._call(start2, end2) <= end2)
