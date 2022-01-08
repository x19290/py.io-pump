from .iopump import IOPump
from ..codecs.utf8 import utf8encode
from io import BytesIO, StringIO
from os import close, pipe, read, write
from nose.tools import eq_
from unittest import TestCase


class T0auto(TestCase):
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
                    (w0, iobj0), (w1, iobj1),
                    (r0, oobj0), (r1, oobj1),
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


class T1manual(TestCase):
    def test0(self):
        r0, w0 = pipe()
        try:
            r1, w1 = pipe()
            try:
                expected = feed = br'01234', br"abcde"
                iobj0, iobj1 = map(tuple, feed)
                oobj0, oobj1 = BytesIO(), BytesIO()

                def makewriter(fd, iobj):
                    def writer():
                        for y in iobj:
                            write(fd, bytes((y,)))
                        close(fd)
                    return writer

                def makereader(fd, oobj):
                    def reader():
                        while True:
                            chunk = read(fd, 8192)
                            if not chunk:
                                break
                            oobj.write(chunk)
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
