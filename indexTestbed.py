import os
for i in range(1,17):
    print("\n===================\nINDEXING TESTBED " + str(i) + "\n===================\n")
    os.system('python3 index.py testbeds/testbed' + str(i))
