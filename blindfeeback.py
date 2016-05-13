#in query.py its a variable at end, results is ordered array
#format: sim rating:id of doc:doc title
#go through results file

import sys
import os
import porter
import StopWord


#first we need to call the normal program so we would hand over to this class

collection = "Terminal_Reality"

# number of docs we take from the list
k = 3
# number of words from the docs
n = 5




def getIndexFile(word):
    p = porter.PorterStemmer()
    sw = StopWord.StopWord()
    #first we need to stem the word
    term = p.stem(word, 0, len(word) - 1)  # stem the search term

    if not os.path.isfile(collection + "_index/" + word):  # if term matches one of the index files
        return
    if sw.isStopWord(term):  # if the term is a stop word- ignore and go onto the next term
        return
    # now what?



# make method to get the list
def runBlindFeedback(doclist):
    # go through the doc ids
    for ext in doclist:
        # get relevant file
        f = open(collection + "document."+ext)
        lines = f.readlines()
        for line in lines:
            sentence = line.split()
            for word in sentence:
                # check if there is an index file
