from .method import catchall
from nose.tools import eq_
from unittest import TestCase


class T0(TestCase):
    def test0(self):
        class Null:
            catchall = catchall

            def __getattr__(self, name):
                try:
                    self.__getattribute__(name)
                except AttributeError:
                    return self.catchall

        expected = feed = Null()
        actual = feed.no_such_method(0, 1, a=2, b=3)
        eq_(expected, actual)
