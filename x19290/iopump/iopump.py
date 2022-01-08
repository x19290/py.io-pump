from ..thread.ttuple import ThreadTuple


class IOPump(ThreadTuple):
    r'''
    an alternative to `select`, `selectors`
    '''
    @staticmethod
    def threads(*routes):
        from io import DEFAULT_BUFFER_SIZE
        from os import read
        from threading import Thread

        def ispair(route):
            try:
                _, _ = route
            except TypeError:
                return False
            else:
                return True

        def readable(fd):
            try:
                read(fd, 0)
            except:
                return False
            else:
                return True

        handlers = tuple(y for y in routes if not ispair(y))
        routes = tuple(y for y in routes if ispair(y))
        wroutes = tuple((fd, iobj) for fd, iobj in routes if not readable(fd))
        rroutes = tuple((fd, oobj) for fd, oobj in routes if readable(fd))

        def readpump(fd, oobj, adapt):
            while True:
                bits = read(fd, DEFAULT_BUFFER_SIZE)
                if not bits:
                    break
                oobj.write(adapt(bits))

        def writepump(fd, iobj):
            from ..codecs.utf8 import utf8encode as adapt
            from os import close, write

            iobj = iobj.__iter__()
            try:
                chunk = iobj.__next__()
            except StopIteration:
                pass
            else:
                try:
                    chunk = adapt(chunk)
                except TypeError:
                    def adapt(b):
                        return b
                write(fd, chunk)
            for chunk in iobj:
                write(fd, adapt(chunk))
            close(fd)

        if rroutes:
            try:
                rroutes[0][1].write(r'')
            except TypeError:
                def adapt(b):
                    return b
            else:
                def adapt(b):
                    from ..codecs.utf8 import utf8decode
                    return utf8decode(b)
            yield from (
                Thread(target=readpump, args=args, kwargs=dict(adapt=adapt))
                for args in rroutes
            )

        yield from (Thread(target=writepump, args=args) for args in wroutes)

        yield from (Thread(target=y) for y in handlers)
