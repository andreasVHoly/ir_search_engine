# import sys
# import subprocess
#
# #
# def constructList(collection, query):
#     splitquery = query.split("and")
#     newquery = []
#     print(splitquery)
#     for i in splitquery:
#         i = i.strip()
#         newquery.append(i)
#     print(newquery)
#     # going to type this so they dpnt steal out ans3wers
#     # u get a query which has an and in it like below
#     # it already splits into seperate terms
#     # so it will split on all and's
#     count = 0
#     #FIX file writing
#     for q in newquery:
# 		fileName = "./Results/boolResults." + str(count)
# 		sys.stdout.write('\r'+ "Getting results for query " + str(i) + ": " + query + (" " * 10))
#
# 		with open(fileName, "w+") as output:
# 			subprocess.call(["python3", "query.py", collection, query], stdout=output);
# 	count += 1
#
#
#
#     # then run the query for each of the seperated queries
#     # then find the docs that are featured in all of the results
#
#
# constructList("this is a and test and what the hell and p")