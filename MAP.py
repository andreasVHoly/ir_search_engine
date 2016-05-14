

class MAP:

    def __init__(self):
        self.results = []

    def calculateMAP(self, results):
        self.results = results
        print("Number of results = " + str(len(self.results)))