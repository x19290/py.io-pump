from .iopump import IOPump
from ..codecs.utf8 import utf8decode, utf8encode
from io import BytesIO, StringIO
from os import close, pipe, read, write
from nose.tools import eq_
from unittest import TestCase


class T0(TestCase):
    def _test(self, io, makereader, makewriter):
        r0, w0 = pipe()
        try:
            r1, w1 = pipe()
            try:
                feed = r'01234', r"abcde"
                if io is BytesIO:
                    expected = tuple(utf8encode(y) for y in feed)
                    feed = (tuple(bytes((c,)) for c in y) for y in expected)
                    feed = tuple(feed)
                    decode = encode = lambda y: y
                else:
                    decode, encode = utf8decode, utf8encode
                    expected = feed
                iobj0, iobj1 = map(tuple, feed)
                oobj0, oobj1 = io(), io()

                if makewriter is None:
                    def makewriter(fd, iobj):
                        def writer():
                            for y in iobj:
                                write(fd, encode(y))
                            close(fd)
                        return writer
                if makereader is None:
                    def makereader(fd, oobj):
                        def reader():
                            while True:
                                chunk = read(fd, 8192)
                                if not chunk:
                                    break
                                oobj.write(decode(chunk))
                        return reader

                IOPump(
                    makewriter(w0, iobj0), makewriter(w1, iobj1),
                    makereader(r0, oobj0), makereader(r1, oobj1),
                ).join()
            finally:
                close(r1)
        finally:
            close(r0)

        actual = oobj0.getvalue(), oobj1.getvalue()
        eq_(expected, actual)

    def test000(self):
        self._test(BytesIO, None, None)

    def test001(self):
        self._test(BytesIO, None, _tuple)

    def test010(self):
        self._test(BytesIO, _tuple, None)

    def test011(self):
        self._test(BytesIO, _tuple, _tuple)

    def test100(self):
        self._test(StringIO, None, None)

    def test101(self):
        self._test(StringIO, None, _tuple)

    def test110(self):
        self._test(StringIO, _tuple, None)

    def test111(self):
        self._test(StringIO, _tuple, _tuple)


def _tuple(fd, ioobj):
    return fd, ioobj
