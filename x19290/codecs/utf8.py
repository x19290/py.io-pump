from codecs import getdecoder, getencoder

_decode, _encode = getdecoder(r'UTF-8'), getencoder(r'UTF-8')


def utf8decode(b):
    return _decode(b)[0]


def utf8encode(s):
    return _encode(s)[0]
