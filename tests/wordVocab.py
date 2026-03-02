import unittest
import griot.char as cT
import griot.word as wT

tinyDataset = 'apple orange banana tangerine, what is love? baby dont hurt me, baby dont hurt me, no more. this is a cool ass message'

class testLooseWordVocab(unittest.TestCase):

    def testTokenizerDetokenizer(self):
        vocab = wT.StrictVocab(nulTok=(0,''))

        vocab.addWords(tinyDataset)

        x = vocab.tokenizeLine(tinyDataset)

        y = vocab.detokenizeLine(x)

        z = vocab.tokenizeLine(y)

        a = vocab.detokenizeLine(z)
    