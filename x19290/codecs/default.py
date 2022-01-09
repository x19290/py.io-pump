from codecs import getdecoder, getencoder
from locale import getdefaultlocale

LANG, ENCODING = getdefaultlocale()

_decode, _encode = getdecoder(ENCODING), getencoder(ENCODING)


def decode(b):
    return _decode(b)[0]


def encode(s):
    return _encode(s)[0]
