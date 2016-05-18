import sys
import subprocess


import os

def constructList(collection, query):
    splitquery = query.split("and")
    newquery = []
    #print(splitquery)
    for i in splitquery:
        i = i.strip()
        newquery.append(i)
    count = 1
    matchNumber = len(newquery)
    for q in newquery:
        #print("calling method with " + str(count) + " and query " + str(q))
        os.system('python3 query.py ' + collection + ' \"' + q + '\"' + "  " + str(count))
        count += 1
    allResults = {}
    resultWeights = {}
    for l in range(1,count):
        f = open("Results/booleanRun."+str(l),"r")
        lines = f.readlines()
        for r in lines:
            split = r.split(",")
            if split[0] in resultWeights:
                resultWeights[split[0]] = eval(resultWeights[split[0]]) + eval(split[1])
            else:
                resultWeights[split[0]] = split[1]

            if split[0] in allResults:
                allResults[split[0]] += 1
            else:
                allResults[split[0]] = 1
        f.close()
    finalResults = {}
    for docsIds in allResults.keys():
        if (allResults[docsIds] == matchNumber):
            finalResults[docsIds] = resultWeights[docsIds]

    final = sorted(finalResults, key=finalResults.__getitem__, reverse=True)
    f = open("csvfilenew.csv", "w")
    for i in range(10):
        print(str(final[i]) + " : " + str(resultWeights[final[i]]))
        f.write(str(final[i]) + "," + str(resultWeights[final[i]])+"\n")
    f.close()

