from nose.tools import eq_
from unittest import TestCase

_STR = r'©'


class _Test:
    @classmethod
    def setUpClass(cls):
        cls.decode, cls.encode = map(staticmethod, (cls.decode, cls.encode))
        cls.bin = _STR.encode(cls.ENCODING)

    def test0decode(self):
        expected = _STR
        actual = self.decode(self.bin)
        eq_(expected, actual)

    def test1encode(self):
        expected = self.bin
        actual = self.encode(_STR)
        eq_(expected, actual)


class T0(_Test, TestCase):
    from .default import decode, encode, ENCODING
