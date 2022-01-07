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

        wroutes = (y for y in routes if y[0])
        rroutes = (y for y in routes if not y[0])
        wroutes = tuple((fd, iobj) for _, fd, iobj in wroutes)
        rroutes = tuple((fd, oobj) for _, fd, oobj in rroutes)

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
            for fd, oobj in rroutes:
                yield Thread(target=readpump, args=(fd, oobj, adapt))

        for fd, iobj in wroutes:
            yield Thread(target=writepump, args=(fd, iobj))
