from .identity import identity, strictidentity
from nose.tools import eq_, raises
from unittest import TestCase


class T0(TestCase):
    @raises(TypeError)
    def test0ng0(self):
        strictidentity(0, 1)

    @raises(TypeError)
    def test0ng1(self):
        strictidentity(0, a=1)

    def test1ok0loose(self):
        expected = feed = None
        actual = identity(feed, 0, 1, a=2, b=3)
        eq_(expected, actual)

    def test1ok1strict(self):
        expected = feed = None
        actual = strictidentity(feed)
        eq_(expected, actual)
