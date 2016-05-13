import nltk

from nltk.corpus import wordnet as wn

class Thesaurus:

    #returns a list of synonyms for the entered word
    def getSynonym(self, word):
        synonyms = []
        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name())
        return synonyms