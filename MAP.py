
import os
import sys
import subprocess

def getDocID(strResult):
    print("x")

#Run the queries in the collection to create files with the results
def runQueries(collection):
    for i in range(1,6):
        fileName = "./Results/results." + str(i)
        fo = open("./" + collection + "/query." + str(i), "r")
        query = fo.readline()

        sys.stdout.write('\r'+ "Getting results for query " + str(i) + ": " + query + (" " * 10))

        with open(fileName, "w+") as output:
            subprocess.call(["python3", "query.py", sys.argv[1], query], stdout=output);

if len(sys.argv)<2:
   print ("Syntax: MAP.py <collection>")
   exit(0)

runQueries(sys.argv[1])
print("")


