from .nop import nop, none
from nose.tools import eq_
from unittest import TestCase


class T0(TestCase):
    def _test(self, feed):
        expected = None
        actual = feed(0, 1, a=2, b=3)
        eq_(expected, actual)

    def test0nop(self):
        self._test(nop)

    def test0none(self):
        self._test(none)
