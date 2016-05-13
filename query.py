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

import parameters

# check parameter for collection name
if len(sys.argv)<3:
   print ("Syntax: index.py <collection> <query>")
   exit(0)
 
# construct collection and query
startTime = time.time()
collection = sys.argv[1]
query = ''
arg_index = 2
while arg_index < len(sys.argv):
   query += sys.argv[arg_index] + ' '
   arg_index += 1

# clean query
if parameters.case_folding:
   query = query.lower () # make query lower case
query = re.sub (r'[^ a-zA-Z0-9]', ' ', query) #converting regular expressions into its characters - e.g. \n \r etc.
query = re.sub (r'\s+', ' ', query)
query_words = query.split (' ')

# create accumulators and other data structures
accum = {}
filenames = []
p = porter.PorterStemmer ()

# get N
f = open (collection+"_index_N", "r")
N = eval (f.read ())
f.close ()

# get document lengths/titles
titles = {}
f = open (collection+"_index_len", "r")
lengths = f.readlines () #an array of all the file titles and their lengths
f.close ()

titleScore = 0

# get index for each term and calculate similarities using accumulators
for term in query_words:
    if term != '':
        if parameters.stemming: #if the stemming parameter is set true
            term = p.stem (term, 0, len(term)-1) #stem the search term
        if not os.path.isfile (collection+"_index/"+term): #if term matches one of the index files
           continue
        f = open (collection+"_index/"+term, "r") #open the index file related to the term being searched
        lines = f.readlines () #read lines from index file --> which file the term occurs in and how many times
        idf = 1
        if parameters.use_idf:
           df = len(lines) #df = document frequency - i.e. how many documents the term appears in
           idf = 1/df #idf = inverse document frequency
           if parameters.log_idf: #if log_idf parameter is set true
              idf = math.log (1 + N/df)
        for line in lines:
            mo = re.match (r'([0-9]+)\:([0-9\.]+)', line)
            if mo:
                file_id = mo.group(1)
                tf = float (mo.group(2)) #tf = term frequency
                if not file_id in accum:
                    accum[file_id] = 0
                if parameters.log_tf: #if log_tf paramter is set true
                    tf = (1 + math.log (tf))
                accum[file_id] += (tf * idf)
                # In general, terms with high tf and low df are good at describing a document
                # and discriminating it from other documents.
                # hence tf*idf (term frequency * inverse document frequency)
        f.close()

        #Caalculate a score for the term being in the title
        for l in lengths:
            mo = re.match (r'([0-9]+)\:([0-9\.]+)\:(.+)', l)
            if mo:
                document_id = mo.group (1)
                length = eval (mo.group (2))
                title = mo.group (3)
                if (term in title.lower()):
                    print("Term: " + term + " --> Title: " + title)
                    titleScore += (1/len(title))
                    print("Title Score: " + str(titleScore))
                    if not document_id in accum:
                        accum[document_id] =0
                    accum[document_id] += titleScore

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
         titles[document_id] = title #populate dictionary of titles related to doc IDs
endTime = time.time()
# print top ten results
result = sorted (accum, key=accum.__getitem__, reverse=True)

numRetrieved = len(result)
print("\n" + str(numRetrieved) + " results (" + str(round(endTime - startTime, 3)) + " seconds)\n")

for i in range (min (numRetrieved, 20)):
   print ("{0:10.8f} {1:5} {2}".format (accum[result[i]], result[i], titles[result[i]]))
