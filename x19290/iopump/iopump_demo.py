#!/usr/bin/env python3


def main():
    print(iopump_demo())


def iopump_demo(argv=None):
    r'''
    To do the following doctest (>>> iopump_demo...), run:
    `python3 -m doctest iopump_demo.py`

    There should be no output.

    >>> iopump_demo(r'<>'.split())
    'abcd'

    >>> iopump_demo(r'<> --bin-in'.split())
    'abcd'

    >>> iopump_demo(r'<> --bin-out'.split())
    b'abcd'

    >>> iopump_demo(r'<> --bin-out --bin-in'.split())
    b'abcd'
    '''

    from pathlib import Path
    from sys import path as pythonpath
    pythonpath[:0] = Path(__file__).absolute().parent.parent.parent.__str__(),

    from x19290.iopump import IOPump
    from argparse import ArgumentParser
    from os import close, pipe, write
    if argv is None:
        from sys import argv

    argp = ArgumentParser()
    argp.add_argument(r'--bin-in', action=r'store_true')
    argp.add_argument(r'--bin-out', action=r'store_true')
    argx = argp.parse_args(argv[1:])

    if argx.bin_in:
        stdin = br"Ab", br"cD"

        def encode(bits):
            return bits
    else:
        stdin = r'Ab', r'cD'

        def encode(str):
            return str.encode()

    if argx.bin_out:
        from io import BytesIO as MemIO
    else:
        from io import StringIO as MemIO

    with MemIO() as stdout:
        r, w = pipe()
        try:
            def writer0():
                for y in stdin:
                    write(w, encode(y.lower()))
                close(w)

            reader0 = r, stdout

            # `pump` becomes a tuple (IOPump) of two threads:
            # - Thread(target=writer0)
            # - Thread(target=defaultreader, args=reader0)
            # IOPump can hold any number of (this time only two) such threads
            pump = IOPump(reader0, writer0)

            # These threads are already started.
            # The following is possible
            pump.join()  # IOPump.join() is inherited from ThureadTuple
            return stdout.getvalue()
        finally:
            close(r)


if __name__ == r'__main__':
    main()
