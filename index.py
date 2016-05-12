# Simple extended boolean search engine: indexer based on cranfield format
# Hussein Suleman
# 21 April 2016

import os
import re
import sys

import porter

import parameters

from os import listdir
from os.path import isfile, join


# check parameter for collection name
if len(sys.argv)==1:
   print ("Syntax: index.py <collection>")
   exit(0)
collection = sys.argv[1]

#get all the files in the directory entered
collectionFile = [f for f in listdir(collection) if isfile(join(collection, f))]

data = {}
titles = {}

#for indexing display
count = 1

#create title and data dictionaries from the files in the given directory
for file in collectionFile:
    progress = "Indexing File: " + str(count)
    sys.stdout.write('\r'+progress)
    fileName = file.split(".")
    if fileName[0] == 'document':
        #read in file
        text_file = open("./" + collection + "/" + file, "r")
        lines = text_file.readlines()
        #add title to dictionary
        titles[fileName[1]] = lines[0].rstrip('\n')
        #add file data to dictionary
        fileData = ''
        for i in range (1, len(lines)):
            fileData += " " + lines[i]
        data[fileName[1]] = fileData
        count+=1
sys.stdout.write('\rIndexed All Files' + (" "*len(progress)))
# document length/title file
g = open(collection + "_index_len", "w")

# create inverted files in memory and save titles/N to file
print("\n\nCreating inverted index...")
index = {}
N = len (data.keys())
p = porter.PorterStemmer ()
for key in data:
    content = re.sub(r'[^ a-zA-Z0-9]', ' ', data[key])
    content = re.sub (r'\s+', ' ', content)
    words = content.split (' ')
    doc_length = 0
    for word in words:
        if word != '':
            if parameters.stemming:
                word = p.stem (word, 0, len(word)-1)
            doc_length += 1
            if not word in index:
                index[word] = {key:1}
            else:
                if not key in index[word]:
                    index[word][key] = 1
                else:
                    index[word][key] += 1
    print (key, doc_length, titles[key], sep=':', file=g)
g.close()
print("Done\n")

# write inverted index to files
print("Writing inverted index to files...")
try:
   os.mkdir (collection+"_index")
except:
   pass
for key in index:
    f = open (collection+"_index/"+key, "w")
    for entry in index[key]:
        print (entry, index[key][entry], sep=':', file=f)
    f.close ()
print("Done\n")

# write N
print("Writing index N...")
f = open (collection+"_index_N", "w")
print (N, file=f)
f.close ()
print("Done\n")

print("Indexing Complete!")
    