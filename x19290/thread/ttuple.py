class ThreadTuple(tuple):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, cls.threads(*args, **kwargs))

    def start(self):
        for y in self:
            y.start()
        return self

    def join(self):
        for y in self:
            y.join()
