# class that handles boolean operator and seperation
import os
# collection - testbed name
# query - query to be split
def constructList(collection, query):
    # split into individual parts
    compwords = [' and ',' vs ',' versus ']

    for compword in compwords:
        if compword in query:
            splitquery = query.split(compword)
    newquery = []
    # strip white space
    for i in splitquery:
        i = i.strip()
        newquery.append(i)
    count = 1
    matchNumber = len(newquery)

    # run query program to get results for each indivdual part of the query
    for q in newquery:
        os.system('python3 query.py ' + collection + ' \"' + q + '\"' + "  " + str(count))
        count += 1

    allResults = {}
    resultWeights = {}

    # we sort through the results that we get from text files
    # check which of the documents are shared amongst the sections
    # we add their hit accuracy up
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

    # we select the documents that were common to both queries
    finalResults = {}
    for docsIds in allResults.keys():
        if allResults[docsIds] == matchNumber:
            finalResults[docsIds] = resultWeights[docsIds]

    # we print the result
    final = sorted(finalResults, key=finalResults.__getitem__, reverse=True)
    f = open("csvfilenew.csv", "w")
    for i in range(0, min(len(final), 10)):
        print(str(resultWeights[final[i]]) + " " +str(final[i]))
        f.write(str(final[i]) + "," + str(resultWeights[final[i]])+"\n")
    f.close()

