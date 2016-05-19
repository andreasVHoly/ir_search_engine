# this class handles the blind relevance feedback

import sys
import os
import porter
import StopWord
import tf_idf
import parameters
import re

# number of docs we take from the list
k = parameters.BRF_no_docs
# number of words from the docs
n = parameters.BRF_no_words

tfidf = tf_idf.tfidf()
p = porter.PorterStemmer()
sw = StopWord.StopWord()

termTFIDF ={}

# applies blind relevance feedback
def runBlindFeedback(collection,doclist,N,query, boolantoken):
    # go through the doc ids
    for docNum in range(min(len(doclist)-1, k)):
        # get relevant file

        ext = doclist[docNum]
        f = open(collection + "/document." + ext, errors='ignore')
        lines = f.readlines()
        for line in lines:
            
            if line == "":
                continue

            # compute tf/idf for each words in the documents
            sentence = line.split()
            for word in sentence:
                # check if there is an index file
                word = word.lower()

                # remove numbers
                if not re.search('[a-zA-Z]', word):
                    continue

                # remove stop words
                if parameters.use_Stopword and parameters.use_largeStopwords and sw.isStopWordLarge(word):
                    continue
                elif parameters.use_Stopword and not parameters.use_largeStopwords and sw.isStopWord(word):
                    continue

                if parameters.stemming:  # if the stemming parameter is set true
                    term = p.stem(word, 0, len(word) - 1)  # stem the search term

                # check if file exists
                if not os.path.isfile(collection + "_index/" + term):  # if term matches one of the index files
                    continue

                # calc TD IDF
                result = tfidf.getblindTFIDF(collection, doclist, term, N)
                if term not in termTFIDF:
                    termTFIDF[term] = result
                else:
                    termTFIDF[term] += result
    # create the new query by expanding it with the new words
    newQuery = ""

    # remove query words from expansion terms
    for i in query:
        if parameters.stemming:  # if the stemming parameter is set true
            i = p.stem(i, 0, len(i) - 1)  # stem the search term
        newQuery += i + " "
        if i in termTFIDF:
            termTFIDF[i] = 0

    result = sorted(termTFIDF, key=termTFIDF.__getitem__, reverse=True)

    for i in range(min(len(result)-1, n)):
        newQuery += result[i] + " "
    # to avoid infinite loop we add an indentifier to tell query that blind relevance feedback has been performed
    newQuery += "##"
    #print(newQuery)
    # run query again with expanded search query
    os.system('python3 query.py ' + collection + ' \"' + newQuery + '\"' + " " + str(boolantoken))
