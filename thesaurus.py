import nltk

from nltk.corpus import wordnet as wn

class Thesaurus:

    def getSynonym(self, word):
        return wn.synsets(word)