class Vocab():
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
        freed  = []