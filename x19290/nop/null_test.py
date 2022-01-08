from .null import nullint, nulltuple, nulllist, nullgen
from nose.tools import eq_, raises
from unittest import TestCase


class T0(TestCase):
    def _eq(self, feed, expected):
        actual = feed(0, 1, a=2, b=3)
        eq_(expected, actual)

    def test0int(self):
        self._eq(nullint, 0)

    def test1tuple(self):
        self._eq(nulltuple, ())

    def test2list(self):
        self._eq(nulllist, [])

    @raises(StopIteration)
    def test3gen(self):
        nullgen(0, 1, a=2, b=3).__next__()
