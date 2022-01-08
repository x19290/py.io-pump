from .bool import false, true
from nose.tools import eq_
from unittest import TestCase


class T0(TestCase):
    def test0(self):
        expected = False, True
        actual = false(0, 1, a=2, b=3), true(4, 5, c=6, d=7)
        eq_(expected, actual)
