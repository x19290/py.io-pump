from . import ThreadTuple
from os import close, pipe, read, write
from nose.tools import eq_
from threading import Thread
from unittest import TestCase


class T0(TestCase):
    def test0(self):
        r, w = pipe()
        actual = []
        feed = br"abcd"
        expected = list(feed)

        class ProdCons(ThreadTuple):
            @staticmethod
            def threads():
                def prod():
                    for y in feed:
                        write(w, br'%c' % y)
                    close(w)

                def cons():
                    while True:
                        c = read(r, 1)
                        if not c:
                            break
                        actual.append(ord(c))

                yield from (Thread(target=y) for y in (prod, cons))

        ProdCons().start().join()
        eq_(expected, actual)
