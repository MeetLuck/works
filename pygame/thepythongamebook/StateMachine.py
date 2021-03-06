''' State and Brain class '''
from random import randint
from vector import Vector
#from gameobjects.vector2 import Vector2
from math import sin,cos,atan2,pi
import copy
GRAD = 2*pi/360

class State(object): # Exploring, Seeking, Hunting
    def __init__(self,name):
        self.name = name
    def doActions(self):        pass
    def checkCondition(self):   pass
    def entryActions(self):     pass
    def exitActions(self):      pass

class Brain(object): # brain
    def __init__(self):
        self.states = {} # store states
        self.activestate = None

    def addState(self,state):
       " add state such as exploring,seeking,hunting to dictionary"
       self.states[state.name] = state

    def think(self):
        #print 'think',self.activestate
        # --- Only continue if there is an active state ---
        if self.activestate is None: return # for spider, leaf
        # --- Perfrom the actions of the active state, and check conditions
        newstate = self.activestate.checkCondition()
        if newstate:
            self.setActiveState(newstate)
        else:
            self.activestate.doActions()

    def setActiveState(self,newstate):
        # exitAction(currentstate) => set activestate => entryAction(newstate)
        if self.activestate:
            self.activestate.exitActions() # when exiting current state
        self.activestate = self.states[newstate]
        self.activestate.entryActions()    # when entering new state

class AIStateExploring(State):

    def __init__(self,ai):
        State.__init__(self,'exploring')
        self.ai = ai

    def randomDirection(self):
        if self.ai.IsOutOfNest(): return
        angle = randint(-15,15)
        self.ai.tankAngle += angle
        self.ai.turretAngle += angle

    def doActions(self):
        # change direction in the 5% change
        if randint(1,20) == 1:
            self.randomDirection()

    def checkCondition(self):
        player = self.ai.world.getCloseEntity('player', self.ai.Vp, self.ai.nestsize) #self.ai.nestsize)
        print 'player',player
        if player is None: return None
        # there is a player nearby
        self.ai.playerID = player.ID
        print 'go hunting',player
        return 'hunting'

    def entryActions(self):
        # start with random speed and direction
        self.ai.speed /= 2.0
        self.randomDirection()

class AIStateHunting(State):
    def __init__(self,ai):
        State.__init__(self,'hunting')
        self.ai = ai
        self.gotkill = False

    def getPlayer(self):
        return self.ai.world.getEntity(self.ai.playerID)

    def doActions(self):
        player = self.getPlayer()
        if player is None: return None
        print '----------------- HUNTING %s ----------------------',player
        self.ai.destination = copy.copy(player.Vp)
        if self.ai.Vp.get_distance_to(player.Vp) < self.ai.nestsize: #/2:
            print 'autotarget',player
            self.ai.autotarget(player)
            if player.health <= 0:
                self.ai.world.removeEntity(player)
                self.getkill = True

    def checkCondition(self):
        if self.gotkill:
            return 'exploring'
        else: # player is alive
            player = self.ai.world.getEntity(self.ai.playerID)
            if player is None:
                return 'exploring'
        return None

#           if player:
#               return None # -> stay in Hunting
#           else: # player is out of range
#               return 'exploring'

    def entryActions(self):
        self.ai.speed *=  2.0
        self.ai.turretTurnSpeed *= 2.0
        self.ai.tankTurnSpeed *= 2.0

    def exitActions(self):
        self.gotkill = False
        self.ai.speed /=  2.0
        self.ai.turretTurnSpeed /= 2.0
        self.ai.tankTurnSpeed /= 2.0
