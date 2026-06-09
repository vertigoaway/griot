import numpy as np
import pickle
import os
import queue
from typing import cast
from typing import Generator
from typing import overload
from typing import Any
import typing

class StrictVocab(): #all strings MUST seperate words with the spacer variable

    padTok : tuple[int,str]
    eomTok : tuple[int,str]
    spacer : str
    freed : list[Any]
    def __init__(self,padTok=(0,'[NIL]'),eomTok=(1,'[END]'),spacer=' ') -> None:
        self.padTok = padTok
        self.eomTok = eomTok
        self.spacer = spacer
        self.vocabArr = np.zeros((2),dtype=np.dtypes.StringDType)

        self.keyArr : dict[str,int] = {padTok[1]:padTok[0],eomTok[1]:eomTok[0]}
        self.freed  = []
        return
    def save(self,path:str) -> None:
        with open(path,'wb') as file:
            pickle.dump((self.vocabArr,self.padTok,self.eomTok,self.freed),file)
        return
    def load(self,path:str) -> None:
        with open(path,'rb') as file:
            self.vocabArr,self.padTok,self.eomTok,self.freed = pickle.load(file)

        return
    def __len__(self) -> int:
        """Get the current length of vocab."""
        return len(self.vocabArr)

    @overload
    def __contains__(self, item: int) -> bool: ...
    @overload
    def __contains__(self, item: str) -> bool: ...

    def __contains__(self, item : int | str) -> bool:
        """Check if the specified token/index is set
        Args:
            item: The token/index to check"""
        if isinstance(item, int):
            try:
                return type(self.vocabArr[item])==int
            except:
                return False
        elif isinstance(item, str):
            return self.keyArr.get(item,self.padTok[0]) != self.padTok[0]
        else:
            raise TypeError
    

    @overload
    def __delitem__(self, key: int) -> None: ...
    @overload
    def __delitem__(self, key: str) -> None: ...

    def __delitem__(self,key : str | int) -> None:
        """Deletes the specified token/index.
        Args:
            key: The token to delete."""
        
        if isinstance(key, int):
            y = self.vocabArr[key]
            self.vocabArr[key] = self.padTok[1]
            self.keyArr[y] = self.padTok[0]
            self.freed.append(key)
        elif isinstance(key, str):
            x = self.keyArr[key]
            self.vocabArr[x] = self.padTok[1]
            self.keyArr[key] = self.padTok[0]
            self.freed.append(x)
        return
    

    @overload
    def __getitem__(self, key: int) -> str: ...
    @overload
    def __getitem__(self, key: str) -> int: ...

    def __getitem__(self, key: int  | str ) -> str | int:
        if isinstance(key,int):
            try:
                return self.vocabArr[key]
            except:
                return self.padTok[1]
        elif isinstance(key,str):
            try:
                return self.keyArr[key] # pyright: ignore[reportReturnType]
            except:
                return self.padTok[0]
        else:
            raise TypeError

    @overload
    def __setitem__(self, key: int, value: str) -> None: ...

    @overload
    def __setitem__(self, key: str, value: int) -> None: ...

    def __setitem__(self, key: int | str, value: int | str) -> None:
        if isinstance(key, int) and isinstance(value, str):

            try:
                self.vocabArr[key] = value
            except:
                self.vocabArr.resize(key+1,refcheck=False)
                self.vocabArr[key] = value
            self.keyArr[value] = key

        elif isinstance(key, str) and isinstance(value, int):

            try:
                self.vocabArr[value] = key
            except:
                self.vocabArr.resize(value+1,refcheck=False)
                self.vocabArr[value] = key
            self.keyArr[key] = value
            
        else:
            raise TypeError
        return
    
    def freeIndices(self) -> Generator[int, None, None]:
        while len(self.freed)>0:
            yield self.freed.pop(0)
        x : int = len(self.keyArr)
        while True:
            if self[x] == self.padTok[1]:
                #elf.keyArr.resize(x,refcheck=False)
                self.vocabArr.resize(x,refcheck=False)
                yield x
            x+=1

    @overload
    def addWords(self, words: list[str | np.str_]) -> None: ...
    @overload
    def addWords(self, words: str | np.str_) -> None: ...

    def addWords(self,words:list[str| np.str_] | str | np.str_) -> None:
        """Adds all words from a list of strings.
        Args:
            words: List of strings with words seperated by spacers."""
        if isinstance(words, str):
            words = cast(list[str],words.split(self.spacer))
        indices : Generator = self.freeIndices()
        for word in words:
            self[next(indices)] = word
        return
    
    def tokenizeLine(self,line:str | np.str_) -> np.ndarray:
        l = line.split(self.spacer)
        out = np.zeros((len(l)+1),dtype=np.int32)
        i=0
        for word in l:
            if len(word)<1:
                continue
            
            out[i] = self.keyArr.get(word,self.padTok[0])
            i+=1
        out[-1] = self.eomTok[0]
        
        return out

    def detokenizeLine(self,line:list[int]|np.ndarray) -> str:
        out = ''
        for index in line:
            out += self.vocabArr[index]+self.spacer
        return out[:-2] #remove last space
    
    @overload
    def tokenizeLines(self,lines:str) -> list[np.ndarray]: ...
    @overload
    def tokenizeLines(self,lines:list[str]) -> list[np.ndarray]: ...

    def tokenizeLines(self,lines:list[str | np.str_] | str | np.str_) -> list[np.ndarray]:
        out = []
        if isinstance(lines,str):
            lines = lines.split(self.eomTok[1])
        for line in lines:
            out.append(self.tokenizeLine(line))
        return out
    

    @overload
    def detokenizeLines(self,lines:list[list[int]]) -> list[str | np.str_]: ...
    @overload
    def detokenizeLines(self,lines:list[int]) -> list[str | np.str_]: ...

    def detokenizeLines(self,lines:list[list[int]] | list[int]) -> list[str | np.str_]:
        out = []
        line : list[int]
        y = lines
        if isinstance(lines,type([[1]])):
            linesy : list[int] = cast(list[int], lines)
            tmp : list[list[int]]= [[]]
            for x in linesy:
                if x == self.eomTok[1]:
                    tmp.append([])
                else:
                    tmp[-1].append(x)
            y = tmp
        y = cast(list[list[int]],y)
        for line in y:
            out.append(self.detokenizeLine(line)) 
        return out
