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

        def defaultreader(fd, oobj):
            from ..codecs.utf8 import utf8decode as adapt
            while True:
                bits = read(fd, DEFAULT_BUFFER_SIZE)
                if not bits:
                    break
                try:
                    oobj.write(adapt(bits))
                except TypeError:
                    from ..nop.identity import strictidentity as adapt
                    oobj.write(adapt(bits))
            while True:
                bits = read(fd, DEFAULT_BUFFER_SIZE)
                if not bits:
                    break
                oobj.write(adapt(bits))

        def defaultwriter(fd, iobj):
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
                    from ..nop.identity import strictidentity as adapt
                write(fd, chunk)
            for chunk in iobj:
                write(fd, adapt(chunk))
            close(fd)

        for route in routes:
            try:
                fd, _ = route
            except:
                yield Thread(target=route)
            else:
                try:
                    read(fd, 0)
                except:
                    target = defaultwriter
                else:
                    target = defaultreader
                yield Thread(target=target, args=route)
