from .iopump import IOPump
from ..codecs.utf8 import utf8encode
from io import BytesIO, StringIO
from os import close, pipe
from nose.tools import eq_
from unittest import TestCase


class T0(TestCase):
    def _test(self, io, expect):
        r0, w0 = pipe()
        try:
            r1, w1 = pipe()
            try:
                feed = r'01234', r'abcde'
                expected = tuple(expect(y) for y in feed)
                iobj0, iobj1 = map(tuple, feed)
                oobj0, oobj1 = io(), io()
                IOPump(
                    (True, w0, iobj0), (True, w1, iobj1),
                    (False, r0, oobj0), (False, r1, oobj1),
                ).join()
            finally:
                close(r1)
        finally:
            close(r0)

        actual = oobj0.getvalue(), oobj1.getvalue()
        eq_(expected, actual)

    def test0(self):
        self._test(BytesIO, utf8encode)

    def test1(self):
        self._test(StringIO, lambda y: y)
