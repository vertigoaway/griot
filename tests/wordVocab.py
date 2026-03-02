import unittest
import griot.word as wT


class testStrictWordVocab(unittest.TestCase):

    def testTokenizerDetokenizer(self):
        tinyDataset = 'apple orange banana tangerine, what is love? baby dont hurt me, baby dont hurt me, no more. this is a cool ass message'
        vocab = wT.StrictVocab(nulTok=(0,''))

        vocab.addWords(tinyDataset)

        x = vocab.tokenizeLine(tinyDataset)
        y = vocab.detokenizeLine(x)
        z = vocab.tokenizeLine(y)
        a = vocab.detokenizeLine(z)
        self.assertEqual(x,z)
        self.assertEqual(y,a)
        self.assertEqual(x,[2, 3, 4, 5, 6, 20, 8, 13, 14, 15, 16, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 1])
        self.assertEqual(y,"apple orange banana tangerine, what is love? baby dont hurt me, baby dont hurt me, no more. this is a cool ass message")
if __name__ == '__main__':
    unittest.main()