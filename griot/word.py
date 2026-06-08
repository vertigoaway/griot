import pickle
from typing import Generator
from typing import cast
from typing import overload

class StrictVocab(): #all strings MUST seperate words with the spacer variable
    vocabDict : dict[str,int]
    tokenDict : dict[int,str]
    padTok : tuple[int,str]
    eomTok : tuple[int,str]
    spacer : str
    freed : list[int]
    def __init__(self,padTok=(0,'[NIL]'),eomTok=(1,'[END]'),spacer=' ') -> None:
        self.padTok = padTok
        self.eomTok = eomTok
        self.spacer = spacer
        self.vocabDict = {padTok[1]:padTok[0],eomTok[1]:eomTok[0]}
        self.tokenDict = {padTok[0]:padTok[1],eomTok[0]:eomTok[1]}
        self.freed  = []
    def save(self,path:str) -> None:
        with open(path,'wb') as file:
            pickle.dump((self.vocabDict,self.padTok,self.eomTok,self.freed),file)
        return
    def load(self,path:str) -> None:
        with open(path,'rb') as file:
            self.vocabDict,self.padTok,self.eomTok,self.freed = pickle.load(file)
        self.tokenDict = {v: k for k, v in self.vocabDict.items()}
        return
    def __len__(self) -> int:
        """Get the current length of vocab."""
        return len(self.vocabDict)

    @overload
    def __contains__(self, item: int) -> bool: ...
    @overload
    def __contains__(self, item: str) -> bool: ...

    def __contains__(self, item : int | str) -> bool:
        """Check if the specified token/index is set
        Args:
            item: The token/index to check"""
        if type(item) == int:
            return type(self.tokenDict.get(item))==int
        elif type(item) == str:
            return type(self.vocabDict.get(item))==str
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
        return
    

    @overload
    def __getitem__(self, key: int) -> str: ...
    @overload
    def __getitem__(self, key: str) -> int: ...

    def __getitem__(self, key: int | str) -> str | int:
        if type(key) == int:
            return self.tokenDict.get(key, self.padTok[1])
        elif type(key) == str:
            return self.vocabDict.get(key, self.padTok[0])
        else:
            raise TypeError

    @overload
    def __setitem__(self, key: int, value: str) -> None: ...

    @overload
    def __setitem__(self, key: str, value: int) -> None: ...

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
            if self.tokenDict.get(x,self.padTok[1]) == self.padTok[1]:
                yield x
            x+=1

    @overload
    def addWords(self, words: list[str]) -> None: ...
    @overload
    def addWords(self, words: str) -> None: ...

    def addWords(self,words:list[str] | str) -> None:
        """Adds all words from a list of strings.
        Args:
            words: List of strings with words seperated by spacers."""
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
            out.append(self.vocabDict.get(word,self.padTok[0]))
        out.append(self.eomTok[0])
        return out

    def detokenizeLine(self,line:list[int]) -> str:
        out = ''
        for index in line:
            out += self.tokenDict.get(index,self.padTok[1])+self.spacer
        return out[:-len(self.eomTok[1]) - 1 - len(self.spacer)] #remove last space
    def tokenizeLines(self,lines:list[str] | str) -> list[list[int]]:
        out = []
        if type(lines)==str:
            lines = lines.split(self.eomTok[1])
        for line in lines:
            out.append(self.tokenizeLine(line))
        return out
    

    @overload
    def detokenizeLines(self,lines:list[list[int]]) -> list[str]: ...
    @overload
    def detokenizeLines(self,lines:list[int]) -> list[str]: ...

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
    padTok : tuple[int,str]
    eomTok : tuple[int,str]
    freed : list[int]
    def __init__(self,padTok=(0,'[NIL]'),eomTok=(1,'[END]')) -> None:
        self.padTok = padTok
        self.eomTok = eomTok
        self.vocabDict = {padTok[1]:padTok[0],eomTok[1]:eomTok[0]}
        self.tokenDict = {padTok[0]:padTok[1],eomTok[0]:eomTok[1]}
        self.freed  = []
    def save(self,path:str) -> None:
        with open(path,'wb') as file:
            pickle.dump((self.vocabDict,self.padTok,self.eomTok,self.freed),file)
        return
    def load(self,path:str) -> None:
        with open(path,'rb') as file:
            self.vocabDict,self.padTok,self.eomTok,self.freed = pickle.load(file)
        self.tokenDict = {v: k for k, v in self.vocabDict.items()}
        return
    def __len__(self) -> int:
        """Get the current length of vocab."""
        return len(self.vocabDict)
    @overload
    def __contains__(self, item: int) -> bool: ...
    @overload
    def __contains__(self, item: str) -> bool: ...

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
    

    @overload
    def __delitem__(self, key: int) -> None: ...
    @overload
    def __delitem__(self, key: str) -> None: ...

    def __delitem__(self,key : str | int) -> None:
        """Deletes the specified token/index.
        Args:
            key: The token to delete."""
        
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
        return
    

    @overload
    def __getitem__(self, key: int) -> str: ...
    @overload
    def __getitem__(self, key: str) -> int: ...

    def __getitem__(self, key: int | str) -> str | int:
        if type(key) == int:
            return self.tokenDict.get(key, self.padTok[1])
        elif type(key) == str:
            return self.vocabDict.get(key, self.padTok[0])
        else:
            raise TypeError

    @overload
    def __setitem__(self, key: int, value: str) -> None: ...

    @overload
    def __setitem__(self, key: str, value: int) -> None: ...

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
            if self.tokenDict.get(x,self.padTok[1]) == self.padTok[1]:
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