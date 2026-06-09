import itertools
import numpy as np
from typing import cast
from typing import overload
from typing import Any
import typing
from collections import Counter
def encodeOneHot():
    raise NotImplementedError

def decodeOneHot():
    raise NotImplementedError



def getAbsPosEncoding(seqLen : int, d : int, n: int = 10000,device=['cpu']):
    """Returns absolute positional encoding matrix
    Args:
        d: Embedding dim size
        seqLen: Size of input sequence
        n: some fuckin parameter"""
    #
    P = np.zeros((seqLen, d), device=device)
    for k in range(seqLen):
        for i in np.arange(int(d/2)):
            denominator = np.power(n, 2*i/d)
            P[k, 2*i] = np.sin(k/denominator)
            P[k, 2*i+1] = np.cos(k/denominator)
    return P

#below code is from https://medium.com/thedeephub/positional-encoding-explained-a-deep-dive-into-transformer-pe-65cfe8cfe10b
#by Nikhil Chowdary Paleti
def getRotaryPosEncoding(context_len: int, d_model: int) -> np.ndarray:
    """
    Generate the Rotary Matrix for ROPE
    Args:
        context_len (int): context len
        d_model (int): embedding dim
    Returns:
        np.ndarray: the rotary matrix of dimension context_len x d_model x d_model
    """
    R = np.zeros((context_len, d_model, d_model))
    positions = np.arange(1, context_len + 1)[:, np.newaxis]
    # Create matrix theta (shape: context_len x d_model // 2)
    slice_i = np.arange(0, d_model // 2)
    theta = 10000. ** (-2.0 * slice_i.astype(float) / d_model)
    m_theta = positions * theta
    # Create sin and cos values
    cos_values = np.cos(m_theta)
    sin_values = np.sin(m_theta)
    # Populate the rotary matrix R using advanced indexing
    R[:, 2*slice_i, 2*slice_i] = cos_values
    R[:, 2*slice_i, 2*slice_i+1] = -sin_values
    R[:, 2*slice_i+1, 2*slice_i] = sin_values
    R[:, 2*slice_i+1, 2*slice_i+1] = cos_values
    return R
#end of imported code

def flattenLines(lines:list[list[Any]]) -> list[Any]:
    return list(itertools.chain.from_iterable(lines))

@overload
def getWordCtr(data:list[list[str]]) -> Counter: ...

@overload
def getWordCtr(data:list[str]) -> Counter: ...

def getWordCtr(data:list[str] | list[list[str]]) -> Counter:
    distrib : list[tuple[str,int]] = []
    
        
    if type(data) == list[list[Any]]:
        data = cast(list[Any],
                    flattenLines(
                        cast(list[list[str]],
                                data
                    )))
    #protective code removed. TODO: add it back!!!    
    return Counter(data)