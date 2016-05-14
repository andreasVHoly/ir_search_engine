import sys
import subprocess

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
    #sys.stdout.write('\r'+ "Calculating MAP..." + (" " * 30))

if len(sys.argv)<2:
   print ("Syntax: NDCG.py <collection>")
   exit(0)

runQueries(sys.argv[1])
getResults("./Results/results.1")
