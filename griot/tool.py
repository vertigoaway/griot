import itertools


def encodeOneHot():
    raise NotImplementedError

def decodeOneHot():
    raise NotImplementedError



def encodePosition():
    raise NotImplementedError
def decodePosition():
    raise NotImplementedError


def flattenTokenizedLines(lines:list[list[int]]):
    return list(itertools.chain.from_iterable(lines))