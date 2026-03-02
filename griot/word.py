import pickle
from typing import Generator
from typing import cast



class StrictVocab(): #all strings MUST seperate words with the spacer variable
    vocabDict : dict[str,int]
    tokenDict : dict[int,str]
    nulTok : tuple[int,str]
    eomTok : tuple[int,str]
    spacer : str
    freed : list[int]
    def __init__(self,nulTok=(0,'[NIL]'),eomTok=(1,'[END]'),spacer=' ') -> None:
        self.nulTok = nulTok
        self.eomTok = eomTok
        self.spacer = spacer
        self.vocabDict = {nulTok[1]:nulTok[0],eomTok[1]:eomTok[0]}
        self.tokenDict = {nulTok[0]:nulTok[1],eomTok[0]:eomTok[1]}
        self.freed  = []
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
            y : str = self.tokenDict[key]
            del self.tokenDict[key]
            del self.vocabDict[y]
            self.freed.append(key)
        elif type(key) == str:
            x : int = self.vocabDict[key]
            del self.vocabDict[key]
            del self.tokenDict[x]
            self.freed.append(x)
        else:
            raise TypeError
        return
    def __getitem__(self, key: int | str) -> int | str:
        if type(key) == int:
            x = self.tokenDict.get(key,self.nulTok[0])
            if x == None:
                return self.nulTok[1]
            return x
        elif type(key) == str:
            x = self.vocabDict.get(key,self.nulTok[0])
            if x == None:
                return self.nulTok[0]
            return x
        else:
            raise TypeError
    def __setitem__(self, key: int | str, value: int | str) -> None:
        if type(key) == int and type(value) == str:
            value = value.strip(self.spacer)
            self.tokenDict[key] = value
            self.vocabDict[value] = key
        elif type(key) == str and type(value) == int:
            key = key.strip(self.spacer) #can't allow words with any spacers, would cause bugs 
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
    def addWords(self,words:list[str] | str) -> None:
        if type(words) == str:
            words = words.split(self.spacer)
        indices = self.freeIndices()
        for word in words:
            self[next(indices)] = word
        return
    
    def tokenizeLine(self,line:str) -> list[int]:
        out : list[int] = []

        for word in line.split(self.spacer):
            if len(word)<1:
                continue
            out.append(self.vocabDict.get(word,self.nulTok[0]))
        out.append(self.eomTok[0])
        return out

    def detokenizeLine(self,line:list[int]) -> str:
        out = ''
        for index in line:
            out += self.tokenDict.get(index,self.nulTok[1])+self.spacer
        return out[:-len(self.eomTok[1]) - 1 - len(self.spacer)] #remove last space
    def tokenizeLines(self,lines:list[str] | str) -> list[list[int]]:
        out = []
        if type(lines)==str:
            lines = lines.split(self.eomTok[1])
        for line in lines:
            out.append(self.tokenizeLine(line))
        return out
    def detokenizeLines(self,lines:list[list[int]] | list[int]) -> list[str]:
        out = []
        line : list[int]
        y = lines
        if type(lines) == list[int]:
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
            out.append(self.detokenizeLine(line)) # pyright: ignore[reportArgumentType]
        return out
    

    
    def lazyTokenizeLines(self,lines:list[str]):
        raise NotImplementedError
    def lazyDetokenizeLines(self,lines:list[list[int]]):
        raise NotImplementedError



class Vocab(): #no spacers, allows encoding parts of words
    vocabDict : dict[str,int]
    tokenDict : dict[int,str]
    nulTok : tuple[int,str]
    eomTok : tuple[int,str]
    freed : list[int]
    def __init__(self,nulTok=(0,'[NIL]'),eomTok=(1,'[END]')) -> None:
        self.nulTok = nulTok
        self.eomTok = eomTok
        self.vocabDict = {nulTok[1]:nulTok[0],eomTok[1]:eomTok[0]}
        self.tokenDict = {nulTok[0]:nulTok[1],eomTok[0]:eomTok[1]}
        self.freed  = []
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
    def addWords(self,words:list[str]) -> None:
        indices = self.freeIndices()
        for word in words:
            self[next(indices)] = word
        return
    




    def lazyTokenizeLines(self,lines:list[str]):
        raise NotImplementedError
    def lazyDetokenizeLines(self,lines:list[list[int]]):
        raise NotImplementedError