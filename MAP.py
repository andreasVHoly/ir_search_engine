import re
import os
import sys
import subprocess

def calcAllMAP():
    totMap = 0
    for i in range(1,6):
        docIDs = getResults("./Results/results." + str(i))
        totMap+=calcMAP(i, docIDs)
    return totMap/5

def calcMAP(q, dIDs):
    map = 0
    pos = 1
    for d in dIDs:
        map += getRel(q, d, pos)
        pos+=1
    map /= len(dIDs)
    return map

def getRel(q, ID, pos):
    fileName = "./" + sys.argv[1] + "/relevance." + str(q)
    fo = open(fileName, "r")
    rel = fo.readlines()

    if int(rel[int(ID)]) == 0:
        return int(rel[int(ID)])/pos
    elif int(rel[int(ID)]) == 1:
        return (int(rel[int(ID)])/pos)*1.5
    elif int(rel[int(ID)]) == 2:
        return 1

def getResults(resultFile):
    dID = []
    fo = open(resultFile, "r")
    lines = fo.readlines()
    for line in lines:
        line = line.rstrip('\n')
        result = line.split(" ")
        if len(result) > 2:
            if result[1] != "results":
                dID.append(result[1])
    return dID

#Run the queries in the collection to create files with the results
def runQueries(collection):
    for i in range(1,6):
        fileName = "./Results/results." + str(i)
        fo = open("./" + collection + "/query." + str(i), "r")
        query = fo.readline()

        sys.stdout.write('\r'+ "Getting results for query " + str(i) + ": " + query + (" " * 10))

        with open(fileName, "w+") as output:
            subprocess.call(["python3", "query.py", sys.argv[1], query], stdout=output);

    sys.stdout.write('\r'+ "All results collected." + query + (" " * 30))
    print("")
    sys.stdout.write('\r'+ "Calculating MAP..." + (" " * 30))

if len(sys.argv)<2:
   print ("Syntax: MAP.py <collection>")
   exit(0)

runQueries(sys.argv[1])
sys.stdout.write('\r'+ "MAP = " + str(calcAllMAP()) + (" " * 10))
print("")


