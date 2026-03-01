import unittest
import griot.char as cT
import griot.word as wT


class testTokenizer(unittest.TestCase):
    def testCharVocabClassDictionarySync(self):

        return
    def testCharVocabClassTokenizationDetokenization(self):
        voc = cT.charVocab()

        voc.addCharacters(list('abcdefghijklmnopqrstuvwxyz '))

        x = voc.tokenizeLine('apple ')
        y = voc.detokenizeLine(x)
        self.assertEqual(x,[28, 13, 13, 17, 24, 2, 1])
        self.assertEqual(y,'apple \n')
        return
    def testCharVocabClassCharacterDuplication(self):

        return