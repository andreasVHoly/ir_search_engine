import sys

class StopWord:

    def isStopWord(self, word):
        stopwordArr = {'I', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'com', 'for', 'from', 'how', 'in', 'is',
                    'it', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who', 'will',
                    'with', 'www'}        
        for sw in stopwordArr:
            if word == sw:
                return True
        return False
    

        