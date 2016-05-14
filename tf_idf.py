import math
import re

import parameters
import thesaurus

class tfidf:

    def __init__(self):
        self.t = thesaurus.Thesaurus()
        self.collection = ""
        self.term = ""
        self.N = 0
        self.lines = []
        self.df = 0
        self.idf = 0
        self.tf = 0
        self.accum = {}

    def getTFIDF(self, collection, term, N, ratio):
        self.collection = collection
        self.term = term
        self.N = N
        f = ""
        try:
            f = open (self.collection+"_index/"+self.term, "r") #open the index file related to the term being searched
        except FileNotFoundError:
            return self.accum
        self.lines = f.readlines () #read lines from index file --> which file the term occurs in and how many times
        self.idf = 1
        if parameters.use_idf:
           self.df = len(self.lines) #df = document frequency - i.e. how many documents the term appears in
           self.idf = 1/self.df #idf = inverse document frequency
           if parameters.log_idf: #if log_idf parameter is set true
              self.idf = math.log (1 + self.N/self.df)

        for line in self.lines:
            mo = re.match (r'([0-9]+)\:([0-9\.]+)', line)
            if mo:
                file_id = mo.group(1)
                self.tf = float (mo.group(2)) #tf = term frequency
                if not file_id in self.accum:
                    self.accum[file_id] = 0
                if parameters.log_tf: #if log_tf paramter is set true
                    self.tf = (1 + math.log (self.tf))
                self.accum[file_id] += (self.tf * self.idf) * ratio
        f.close()
        return self.accum

    def addTFIDFSysnonyms(self, synTerm, numSyn):
        #similarityRatio = self.t.getSimilarityRatio(self.term, synTerm)
        similarityRatio = 1/numSyn
        #print(synTerm + " Similarity Ratio = " + str(similarityRatio))
        self.accum = self.getTFIDF(self.collection, synTerm, self.N, similarityRatio)