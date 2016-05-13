import nltk
import porter
import parameters

from nltk.corpus import wordnet as wn

class Thesaurus:

    #returns a list of synonyms for the entered word
    def getSynonym(self, word):
        synonyms = []
        p = porter.PorterStemmer ()
        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                syn = lemma.name()
                if parameters.stemming: # stem sysnonym if stemming parameter is set True.
                    syn = p.stem (lemma.name(), 0, len(lemma.name())-1)
                if syn not in synonyms:
                    synonyms.append(syn)
        return synonyms