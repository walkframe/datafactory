# coding: utf-8

from unittest import TestCase

if bytes is str:
    a = '1'
else:
    a = '1'.encode('utf8')


class TestHashField(TestCase):
    def _get_class(self, *args, **kwargs):
        from datafactory.fields.hashof import HashOfField as Field
        return Field(*args, **kwargs)

    def test_hash_field_normal(self):
        import hashlib
        field = self._get_class('a', 'md5')

        record = {'a': 1}
        value = field(record)
        self.assertEqual(
            value,
            hashlib.md5(a).hexdigest()
        )
