import sys
import subprocess
import math


def calcTotDCG():
    totDCG = 0
    for i in range(1,6):
        docIDs = getResults("./Results/results." + str(i))
        dcg = calcDCG(i, docIDs)
        arrNDCG.append(dcg)
        print("Query " + str(i) + " DCG = " + str(dcg))
        totDCG+=dcg
    print("")
    return totDCG/5

def calcDCG(q, dIDs):
    DCG = 0
    pos = 1
    for d in dIDs:
        DCG += getRel(q, d)/(math.log2(pos+1))
        pos+=1
    return DCG

def calcTotIDCG():
    totIDCG = 0
    for i in range(1,6):
        docIDs = getResults("./Results/results." + str(i))
        for x in range(0,len(docIDs)):
            for y in range(0, len(docIDs)-1):
                if getRel(i, docIDs[y]) < getRel(i, docIDs[y+1]):
                    temp = docIDs[y]
                    docIDs[y] = docIDs[y+1]
                    docIDs[y+1] = temp
        idcg = calcDCG(i, docIDs)
        arrNDCG[i-1] /= idcg
        print("Query " + str(i) + " IDCG = " + str(idcg))
        totIDCG+=idcg
    print("")
    return totIDCG/5

def getRel(q, ID):
    fileName = "./" + sys.argv[1] + "/relevance." + str(q)
    fo = open(fileName, "r")
    rel = fo.readlines()
    return int(rel[int(ID)])

#Get document IDs from the results files
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

if len(sys.argv)<2:
   print ("Syntax: NDCG.py <collection>")
   exit(0)

runQueries(sys.argv[1])
arrNDCG = []
finalDCG = calcTotDCG()
finalIDCG = calcTotIDCG()
NDCG = finalDCG/finalIDCG

for i in range(0,5):
    print("Query " + str(i+1) + " NDCG = " + str(arrNDCG[i]))
print("\nDCG = " + str(finalDCG) + "   IDCG = " + str(finalIDCG) + "   NDCG = " + str(NDCG))

