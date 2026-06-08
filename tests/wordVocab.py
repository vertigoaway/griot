import unittest
import griot.word as wT


class testStrictWordVocab(unittest.TestCase):

    def testTokenizerDetokenizer(self):
        tinyDataset = 'apple orange banana tangerine, what is love? baby dont hurt me, baby dont hurt me, no more. this is a cool ass message'
        vocab = wT.StrictVocab(padTok=(0,''))

        vocab.addWords(tinyDataset)

        tokenizedDataset = vocab.tokenizeLine(tinyDataset)
        dataset1Pass = vocab.detokenizeLine(tokenizedDataset)
        tokenized1Pass = vocab.tokenizeLine(dataset1Pass)
        dataset2Pass = vocab.detokenizeLine(tokenized1Pass)
        self.assertEqual(tokenizedDataset,tokenized1Pass)
        self.assertEqual(dataset1Pass,dataset2Pass)
        self.assertEqual(tokenizedDataset,[2, 3, 4, 5, 6, 20, 8, 13, 14, 15, 16, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 1])
        self.assertEqual(dataset1Pass,"apple orange banana tangerine, what is love? baby dont hurt me, baby dont hurt me, no more. this is a cool ass message")
if __name__ == '__main__':
    unittest.main()