from typing import Generator
import os
import queue
class Vocab():
    vocabDict : dict[str,int]
    tokenDict : dict[int,str]
    nulTok : tuple[int,str]
    eomTok : tuple[int,str]
    freed : list[int]
    def __init__(self,nulTok=(0,'�'),eomTok=(1,'\n')) -> None:
        self.nulTok = nulTok
        self.eomTok = eomTok
        self.vocabDict = {nulTok[1]:nulTok[0],eomTok[1]:eomTok[0]}
        self.tokenDict = {nulTok[0]:nulTok[1],eomTok[0]:eomTok[1]}
        self.freed = []
        return
    def __len__(self) -> int:
        """Get the current length of vocab."""
        return len(self.vocabDict)
    def __contains__(self, item : int | str) -> bool:
        """Check if the specified token/index is set
        Args:
            item: The token/index to check"""
        if type(item) == int:
            return type(self.tokenDict.get(item))==int
        elif type(item) == str:
            return self.vocabDict.get(item)==str
        else:
            raise TypeError
    def __delitem__(self, key : int | str) -> None:
        """Deletes the specified token/index.
        Args:
            key: The token/index to delete."""
        if type(key) == int:
            x = self.tokenDict[key]
            del self.tokenDict[key]
            del self.vocabDict[x]
            self.freed.append(key)
        elif type(key) == str:
            x = self.vocabDict[key]
            del self.vocabDict[key]
            del self.tokenDict[x]
            self.freed.append(x)
        else:
            raise TypeError
        return
    def __getitem__(self, key: int | str) -> int | str:
        if type(key) == int:
            x = self.tokenDict.get(key)
            if x == None:
                return self.nulTok[1]
            return x
        elif type(key) == str:
            x = self.vocabDict.get(key)
            if x == None:
                return self.nulTok[0]
            return x
        else:
            raise TypeError
    def __setitem__(self, key: int | str, value: int | str) -> None:
        if type(key) == int and type(value) == str:
            self.tokenDict[key] = value
            self.vocabDict[value] = key
        elif type(key) == str and type(value) == int:
            self.tokenDict[value] = key
            self.vocabDict[key] = value
        else:
            raise TypeError
        return
    def freeIndices(self) -> Generator[int]:
        while len(self.freed)>0:
            yield self.freed.pop(0)
        x : int = len(self.tokenDict)
        while True:
            if self.tokenDict.get(x) == None:
                yield x
                x+=1

    def addCharacters(self, chrs : list[str]) -> None:
        indices = self.freeIndices()
        for c in chrs:
            self[next(indices)] = chrs.pop(-1)
        return
    def tokenizeLine(self,chrs:str)-> list[int]: 
        out : list[int]= []
        for c in chrs:
            out.append(self.vocabDict.get(c)) # pyright: ignore[reportArgumentType]
        out.append(self.eomTok[0])
        return out
    def tokenizeLines(self,lines:list[str]) -> list[list[int]]:
        out : list[list[int]]  = []
        for line in lines:
            out.append(self.tokenizeLine(line))
        return out
    def detokenizeLine(self,toks:list[int]) -> str:
        out : str = ''
        for tok in toks:
            out+=self.tokenDict.get(tok,self.nulTok[1])
        return out
    def detokenizeLines(self,toksList:list[list[int]]) -> list[str]:
        out : list[str] = []
        for toks in toksList:
            out.append(self.detokenizeLine(toks))
        return out
    def lazyTokenizeLines(self,lines:list[str]):
        raise NotImplemented
    def lazyDetokenizeLines(self,):
        raise NotImplemented