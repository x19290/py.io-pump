from .utf8 import utf8decode, utf8encode
from nose.tools import eq_
from unittest import TestCase

_STR = r'©'


class _Test:
    @classmethod
    def setUpClass(cls):
        cls.bin = _STR.encode(cls.encoding)
        cls.decode, cls.encode = map(staticmethod, cls.codecs)

    def test0decode(self):
        expected = _STR
        actual = self.decode(self.bin)
        eq_(expected, actual)

    def test1encode(self):
        expected = self.bin
        actual = self.encode(_STR)
        eq_(expected, actual)


class T0utf8(_Test, TestCase):
    encoding = r'UTF-8'
    codecs = utf8decode, utf8encode
