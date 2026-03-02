from typing import Generator
import pickle
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
    def save(self,path:str) -> None:
        with open(path,'wb') as file:
            pickle.dump((self.vocabDict,self.nulTok,self.eomTok,self.freed),file)
        return
    def load(self,path:str) -> None:
        with open(path,'rb') as file:
            self.vocabDict,self.nulTok,self.eomTok,self.freed = pickle.load(file)
        self.tokenDict = {v: k for k, v in self.vocabDict.items()}
        return
    def __len__(self) -> int:
        """Get the current length of vocab."""
        return len(self.vocabDict)
    def __contains__(self, item : int | str) -> bool:
        """Check if the specified token/index is set
        Args:
            item: The token/index to check"""
        if type(item) == int:
            return type(self.tokenDict.get(item,self.nulTok[0]))==int
        elif type(item) == str:
            return self.vocabDict.get(item,self.nulTok[1])==str
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
            y = self.vocabDict[key]
            del self.vocabDict[key]
            del self.tokenDict[y]
            self.freed.append(y)
        else:
            raise TypeError
        return
    def __getitem__(self, key: int | str) -> int | str:
        if type(key) == int:
            x = self.tokenDict.get(key,self.nulTok[1])
            if x == None:
                return self.nulTok[1]
            return x
        elif type(key) == str:
            y = self.vocabDict.get(key,self.nulTok[0])
            if y == None:
                return self.nulTok[0]
            return y
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
    def freeIndices(self) -> Generator[int, None, None]:
        while len(self.freed)>0:
            yield self.freed.pop(0)
        x : int = len(self.tokenDict)
        while True:
            if self.tokenDict.get(x,self.nulTok[1]) == self.nulTok[1]:
                yield x
                x+=1

    def addCharacters(self, chrs : list[str]) -> None:
        indices = self.freeIndices()
        for c in chrs:
            self[next(indices)] = c
        return
    def tokenizeLine(self,chrs:str)-> list[int]: 
        out : list[int]= []
        for c in chrs:
            out.append(self.vocabDict.get(c, self.nulTok[0])) # pyright: ignore[reportArgumentType]
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
        raise NotImplementedError
    def lazyDetokenizeLines(self,lines:list[list[int]]):
        raise NotImplementedError