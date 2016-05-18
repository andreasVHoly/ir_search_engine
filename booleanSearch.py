import sys
import subprocess

import os

def constructList(collection, query):
    #print("***boolean search class called ")
    splitquery = query.split("and")
    newquery = []
    #print(splitquery)
    for i in splitquery:
        i = i.strip()
        newquery.append(i)
    #print("final query is " + str(newquery))
    count = 1
    #FIX file writing
    matchNumber = len(newquery)
    #print("**number of terms to match " + str(matchNumber))
    #print("**query terms " + str(newquery))
    for q in newquery:
        #print("calling method with " + str(count) + " and query " + str(q))
        os.system('python3 query.py ' + collection + ' \"' + q + '\"' + "  " + str(count))
        #print("Method done")
        count += 1
    #print("at this stage")
    allResults = {}
    resultWeights = {}
    #print("count is " + str(count))
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
            #print("**doc hit: " + str(docsIds) + " with hits: " + str(allResults[docsIds]))
            finalResults[docsIds] = resultWeights[docsIds]

    print
    final = sorted(finalResults, key=finalResults.__getitem__, reverse=True)
    #print(final)
    f = open("csvfilenew.csv", "w")
    for i in range(10):
        #print( str(resultWeights[final[i]]))
        print(str(final[i]) + " : " + str(resultWeights[final[i]]))
        f.write(str(final[i]) + "," + str(resultWeights[final[i]])+"\n")
    f.close()

#constructList("Terminal Reality", "this is a and test and what the hell and p")