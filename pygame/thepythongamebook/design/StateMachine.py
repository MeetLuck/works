''' State and Brain class '''
from constants import *
import copy
GRAD = 2*pi/360

class State(object): # Exploring, Seeking, Hunting
    def __init__(self,name):
        self.name = name
    def doActions(self):        pass
    def checkCondition(self):   pass
    def entryActions(self):     pass
    def exitActions(self):      pass

    def getPlayer(self):
        player = self.ai.world.getCloseEntity('player', self.ai.Vp, 2*self.ai.nestsize) #self.ai.nestsize)
        return player
    def randomDirection(self):
        self.ai.turndirection = randint(-1,1) 

class Brain(object): # brain
    def __init__(self):
        self.states = {} # store states
        self.activestate = None

    def addState(self,state):
       " add state such as exploring,seeking,hunting to dictionary"
       self.states[state.name] = state

    def think(self):
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
        self.world = self.ai.world

    def doActions(self):
        # change direction in the 5% change
        if randint(1,10) == 1:
            self.randomDirection()

    def checkCondition(self):
        if self.ai.IsOutOfNest():
            return 'home'
        player = self.getPlayer()
        if player:
            # there is a player nearby
            self.ai.playerID = player.ID
            return 'hunting'
        return None # back to Exploring

    def entryActions(self):
        self.ai.resetSpeed()
        self.ai.turretAngle = self.ai.tankAngle
        self.randomDirection()

class AIStateHome(State):

    def __init__(self,ai):
        State.__init__(self,'home')
        self.ai = ai
        self.world = self.ai.world

    def doActions(self):
        if self.ai.IsOutOfNest():
            delta =  self.ai.nestposition - self.ai.Vp
            targetAngle = atan2(-delta.y,delta.x)/pi * 180
            diffAngle = targetAngle - self.ai.tankAngle
            if diffAngle < 0: 
                diffAngle += 360
            diffAngle = diffAngle % 360
            #self.tankAngle += diffAngle
            if abs(diffAngle) < 30:
                self.ai.turndirection = 0
                self.ai.speed = 2*self.ai.__class__.speed 
            else: 
                self.ai.turndirection = 4 
                #self.ai.speed = 0.5* self.ai.__class__.speed
                self.ai.speed = 1.0 * self.ai.__class__.speed 
                print 'home diffAngle', diffAngle
            logging.debug('targetAngle: %s' %targetAngle)
            logging.debug('tankAngle: %s' %self.ai.tankAngle)
            logging.debug('diffAngle: %s' %diffAngle)
            logging.debug('delta: %s' %delta)

    def checkCondition(self):
        if self.ai.IsOutOfNest():
            return None # return to "home state"
        player = self.getPlayer()
        print 'player',player
        if player is None: return 'exploring'
        # there is a player nearby
        self.ai.playerID = player.ID
        print 'go hunting',player
        return 'hunting'

    def entryActions(self):
        self.ai.turretAngle = self.ai.tankAngle
    def exitAction(self):
        self.ai.resetSpeed()


class AIStateHunting(State):
    def __init__(self,ai):
        State.__init__(self,'hunting')
        self.ai = ai
        self.world = self.ai.world
        self.gotkill = False

    def doActions(self):
        player = self.getPlayer()
        if player is None: return
        print '----------------- HUNTING %s ----------------------',player
        distance = self.ai.Vp.get_distance_to(player.Vp) #< 2.0*self.ai.nestsize: #/2:
        print 'distance to player => ',distance
        print 'autotarget =>',player
        self.ai.autorotateTank(player)
        self.ai.autotarget(player)
        if player.health <= 0:
            self.ai.world.removeEntity(player)
            self.getkill = True

    def checkCondition(self):
#       if self.ai.IsOutOfNest():
#           return 'home'
        distance = self.ai.Vp.get_distance_to(self.ai.nestposition) #< 2.0*self.ai.nestsize: #/2:
        if distance > self.ai.nestsize * 3.5:
            return 'home'
        if self.gotkill:
            return 'exploring'
        player = self.getPlayer()
        if player is None:
            return 'exploring'
        else:
            return None

    def entryActions(self):
        self.ai.resetSpeed()

    def exitActions(self):
        self.gotkill = False
