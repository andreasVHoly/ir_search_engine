#in query.py its a variable at end, results is ordered array
#format: sim rating:id of doc:doc title
#go through results file

import sys
import os
import porter
import StopWord
import tf_idf
import parameters

#first we need to call the normal program so we would hand over to this class



# number of docs we take from the list
k = 10
# number of words from the docs
n = 6

tfidf = tf_idf.tfidf()
p = porter.PorterStemmer()
sw = StopWord.StopWord()

termTFIDF ={}

# make method to get the list
def runBlindFeedback(collection,doclist,N,query):
    # go through the doc ids
    for docNum in range(min(len(doclist)-1, k)):
        # get relevant file

        ext = doclist[docNum]
        f = open(collection + "/document." + ext, errors='ignore')
        lines = f.readlines()
        for line in lines:
            sentence = line.split()
            for word in sentence:
                # check if there is an index file
                word = word.lower()

                if parameters.use_Stopword and parameters.use_largeStopwords and sw.isStopWordLarge(word):
                    #print("Skipped stopword " + word)
                    continue
                elif parameters.use_Stopword and not parameters.use_largeStopwords and sw.isStopWord(word):
                    # print("Skipped stopword " + word)
                    continue

                if parameters.stemming:  # if the stemming parameter is set true
                    term = p.stem(word, 0, len(word) - 1)  # stem the search term

                #print(collection + "_index/" + term)
                if not os.path.isfile(collection + "_index/" + term):  # if term matches one of the index files
                    continue
                #print("looking up index file for term " + term)
                result = tfidf.getblindTFIDF(collection, doclist, term, N)
                if term not in termTFIDF:
                    termTFIDF[term] = result
                else:
                    termTFIDF[term] += result
                #no we need to calc tf and idf
    #print(termTFIDF)
    newQuery = ""
    #remove query words from expansion terms
    for i in query:
        if parameters.stemming:  # if the stemming parameter is set true
            i = p.stem(i, 0, len(i) - 1)  # stem the search term
        newQuery += i + " "
        if i in termTFIDF:
            termTFIDF[i] = 0
    result = sorted(termTFIDF, key=termTFIDF.__getitem__, reverse=True)
    #print(result)
    for i in range(min(len(result)-1, n)):
        #print(result[i])
        newQuery += result[i] + " "
    # to avoid infinite loop
    newQuery += "##"
    #print("new search query: " + newQuery)
    os.system('python3 query.py ' +  collection + ' \"'  + newQuery + '\"')