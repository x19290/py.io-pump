#!/usr/bin/env python3

from pathlib import Path
from sys import path as pythonpath
pythonpath[:0] = Path(__file__).absolute().parent.parent.parent.__str__(),
from x19290.thread import ThreadTuple


def main():
    print(ttuple_demo())


def ttuple_demo():
    r'''
    To do the following doctest (>>> ttuple_demo...), run:
    `python3 -m doctest ttuple_demo.py`

    There should be no output.

    >>> ttuple_demo()
    b'abcd'
    '''

    from pathlib import Path
    from io import BytesIO
    from os import close, pipe, read, write

    iobj = b"Ab", b"cD"
    r, w = pipe()
    try:
        with BytesIO() as oobj:
            pump = _Pump(iobj, w, r, oobj)
            # `p` becomes a tuple (_Pump) of two threads:
            # - Thread(target=writer0)
            # - Thread(target=reader0)
            # ThreadTuple can hold any number of (this time only two)
            # such threads
            pump.start().join()
            return oobj.getvalue()
    finally:
        close(r)


class _Pump(ThreadTuple):
    @staticmethod
    def threads(iobj, w, r, oobj):
        from threading import Thread

        def writer(iobj=iobj, w=w):
            from os import close, write

            for y in iobj:
                write(w, y.lower())
            close(w)

        def reader(r=r, oobj=oobj):
            from os import read

            while True:
                data = read(r, 8192)
                if not data:
                    break
                oobj.write(data)

        yield Thread(target=reader)
        yield Thread(target=writer)


if __name__ == r'__main__':
    main()
