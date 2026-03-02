import unittest
import griot.char as cT
import griot.word as wT


class testTokenizer(unittest.TestCase):
    def testCharVocabClassDictionarySync(self):

        return
    def testCharVocabClassTokenizationDetokenization(self):
        voc = cT.Vocab()

        voc.addCharacters(['a','p','l','e',' '])
        print(voc.vocabDict)

        x = voc.tokenizeLine('apple ')
        y = voc.detokenizeLine(x)
        self.assertEqual(x,[2,3,3,4,5,6,1])
        self.assertEqual(y,'apple \n')
        return
    def testCharVocabClassCharacterDuplication(self):

        return
    
if __name__ == '__main__':

    unittest.main()