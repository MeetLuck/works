# Listing 7-6 Base Class for a State
class State(object):
    def __init__(self,name):
        self.name = name
    def doActions(self):
        pass
    def checkConditions(self):
        pass
    def entryActions(self):
        pass
    def exitActions(self):
        pass
