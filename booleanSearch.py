

#
def constructList(query):
    splitquery = query.split("and")
    newquery = []
    print(splitquery)
    for i in splitquery:
        i = i.strip()
        newquery.append(i)
    print(newquery)


constructList("this is a and test and what the hell and p")