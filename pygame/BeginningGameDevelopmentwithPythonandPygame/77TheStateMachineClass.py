# Listing 7-7 The State Machine class

class StateMachine(object):
    def __init__(self):
        self.states = {} # stores the states
        self.activestate = None # current active state
    def addState(self,state):
        # add a state to the internal dictionary
        self.states[state.name] = state
    def think(self):
        # only continues if there is an active state
        if self.activestate is None: return
        # perform the actions of the active state, and check conditions
        self.activestate.doActions()
        newstate_name = self.activestate.checkConditions()
        if newstate_name is not None:
            self.setState(newstate_name)
    def setState(self,newstate_name):
        # change states and perform any exit / entry actions
        if self.activestate is not None:
            self.activestate.exitActions()
        self.activestate = self.states[newstate_name]
        self.activestate.entryActions()
