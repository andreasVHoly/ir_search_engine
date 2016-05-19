# Simple extended boolean search engine: query module
# Hussein Suleman
# 14 April 2016

import re
import math
import sys
import os
import time
import decimal

import porter
import StopWord
import thesaurus
import tf_idf
#import MAP

import parameters

import blindfeeback as blind
import booleanSearch

def getTitle(line):
    pos = line.find("\n")
    if "\n" in line and pos < 40:
        if line[:pos] == "":
            return "<no title>"
        else:
            return line[:pos]
    else:
        if line[:40] == "":
            return "<no title>"
        else:
            return line[:40]


compwords = [' and ',' vs ',' versus ']


# check parameter for collection name
#todo changed here: args to 4 and added new error msg
if len(sys.argv)<4:
   print ("Syntax: query.py <collection> <query> <num for booleansearch (0 if not intended)>")
   exit(0)



# construct collection and query
startTime = time.time()
collection = sys.argv[1]
query = ''
arg_index = 2
while arg_index < len(sys.argv)-1:
   query += sys.argv[arg_index] + ' '
   arg_index += 1


#todo added this
booleantoken = sys.argv[arg_index]

# clean query
if parameters.case_folding:
   query = query.lower () # make query lower case

# if we find a ## token we have already performed blind relevance feedback
if "##" in query:
    parameters.use_blindRelevance = False


query = re.sub (r'[^ a-zA-Z0-9]', ' ', query) #converting regular expressions into its characters - e.g. \n \r etc.
query = re.sub (r'\s+', ' ', query)
query_words = query.split (' ')

# checking if we are performing a boolean search
#todo added this if satement
if eval(booleantoken) == 0:
    parameters.booleanRun = False
else:
    parameters.booleanRun = True

ranBooleanResults = False

# if we find an and and are using boolean feature
#todo modified this if statement
#print("query we are looking at: " + str(query))
for compword in compwords:
    if compword in query and parameters.use_booleanSearch:
        booleanSearch.constructList(collection,query)
        parameters.use_blindRelevance = False
        ranBooleanResults = True



# create accumulators and other data structures
accum = {}
filenames = []
tfidfterms = {}
p = porter.PorterStemmer ()
sw = StopWord.StopWord()
t = thesaurus.Thesaurus()
tfidf = tf_idf.tfidf()

# get N
f = open(collection+"_index_N", "r")
N = eval(f.read())
f.close()




# get document lengths/titles
titles = {}
f = open(collection+"_index_len", "r")
lengths = f.readlines () #an array of all the file titles and their lengths
f.close()

titleScore = 0

# get index for each term and calculate similarities using accumulators
for term in query_words:

    if term != '':
        if parameters.stemming: #if the stemming parameter is set true
            term = p.stem (term, 0, len(term)-1) #stem the search term
        if not os.path.isfile (collection+"_index/"+term): #if term matches one of the index files
           continue
        if parameters.use_Stopword and parameters.use_largeStopwords and sw.isStopWordLarge(term):
            continue
        elif parameters.use_Stopword and not parameters.use_largeStopwords and sw.isStopWord(term):
            continue
        syns = t.getSynonym(term) # get synonyms for the search term
        accum = tfidf.getTFIDF(collection, term, N, 1)



        #todo SYNONYMS
        if parameters.use_thesaurus:
            for s in syns:
                tfidf.addTFIDFSysnonyms(s, len(syns))


        #Caalculate a score for the term being in the title
        # titleMatchCount = 0
        # for l in lengths:
        #     mo = re.match (r'([0-9]+)\:([0-9\.]+)\:(.+)', l)
        #     if mo:
        #         document_id = mo.group (1)
        #         length = eval (mo.group (2))
        #         title = mo.group (3)
        #         if (term in title.lower()):
        #             titleMatchCount += 1
        #             #titleScore += (1/len(title))*titleMatchCount
        #             titleScore += (titleMatchCount/len(title))
        #             if not document_id in accum:
        #                 accum[document_id] =0
        #             accum[document_id] += titleScore

# parse lengths data and divide by |N| and get titles
for l in lengths:
   mo = re.match (r'([0-9]+)\:([0-9\.]+)\:(.+)', l)
   if mo:
      document_id = mo.group (1)
      length = eval (mo.group (2))
      title = mo.group (3)
      if document_id in accum:
         if parameters.normalization: #if the normalize parameter is set true
            accum[document_id] = accum[document_id] / length #calculate similarity of doc to term
         #titles[document_id] = title #populate dictionary of titles related to doc IDs
      titles[document_id] = getTitle(title) #populate dictionary of titles related to doc IDs


result = sorted (accum, key=accum.__getitem__, reverse=True)
# result is a list of doc id's ordered according to highest similarity



if parameters.use_blindRelevance:
    endTime = time.time()
    numRetrieved = len(result)
    # expand query with blind relevance feedback
    blind.runBlindFeedback(collection, result, N, query_words, booleantoken)
else:
    endTime = time.time()
    numRetrieved = len(result)

    # if we are on a boolean and run we create a file with results
    if parameters.booleanRun:
        f = open("Results/booleanRun."+booleantoken,"w")
        for r in result:
            f.write(r+","+str(accum[r])+"\n")

    # if we have already run boolean results
    if not ranBooleanResults:
        f = open("csvfileold.csv", "w")
        for i in range(min(numRetrieved, 10)):
            print("{0:10.8f} {1:5} {2}".format(accum[result[i]], result[i], titles[result[i]]))
            f.write(str(result[i]) + "," + str(accum[result[i]])+"\n")
        f.close()



