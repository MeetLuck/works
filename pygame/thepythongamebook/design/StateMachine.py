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

    def getClosePlayer(self):
        player = self.ai.world.getCloseEntity('player', self.ai.Vp, 2.0*self.ai.nestsize) #self.ai.nestsize)
        return player

    def randomDirection(self):
        delta =  self.ai.Vp - self.ai.nestposition
        if abs(delta.get_magnitude()) < self.ai.nestsize * 0.8:
            self.ai.tankturndirection = randint(-15,15) 
            deltaAngle = self.ai.tankturndirection * self.ai.tankTurnSpeed
            self.ai.tankAngle   += deltaAngle 
            self.ai.turretAngle += deltaAngle

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

    def doActions(self):
        # change direction in the 5% change
        if randint(1,10) == 1:
            self.randomDirection()

    def checkCondition(self):
        if self.ai.IsOutOfNest():
            return 'home'
        player = self.getClosePlayer()
        if player: # there is a player nearby
            self.ai.playerID = player.ID
            return 'hunting'
        else:
            return None # back to Exploring

    def entryActions(self):
        self.ai.resetSpeed()
        self.ai.turretAngle = self.ai.tankAngle
        self.randomDirection()

class AIStateHome(State):

    def __init__(self,ai):
        State.__init__(self,'home')
        self.ai = ai

    def getdiffAnglefromNest(self):
        delta =  self.ai.nestposition - self.ai.Vp
        targetAngle = atan2(-delta.y,delta.x)/pi * 180
        diffAngle = targetAngle - self.ai.tankAngle
        if diffAngle < 0: 
            diffAngle += 360
        diffAngle = diffAngle % 360
        return diffAngle

    def doActions(self):
        if not self.ai.IsOutOfNest(): return
        # ai out of its nest
        diffAngle = self.getdiffAnglefromNest()
        #self.tankAngle += diffAngle
        if abs(diffAngle) <= 15*2:
            self.ai.tankturndirection = 0
            #self.ai.speed  = self.ai.__class__.speed * 1.5 
        else:
            self.ai.tankturndirection = +15

        deltaAngle = self.ai.tankturndirection * self.ai.tankTurnSpeed
        self.ai.tankAngle += deltaAngle
        self.ai.turretAngle += deltaAngle

        logging.debug('tankAngle: %s' %self.ai.tankAngle)
        logging.debug('diffAngle: %s' %diffAngle)

    def checkCondition(self):
        if self.ai.IsOutOfNest():
            return None # return to "home state"
        else:
            player = self.getClosePlayer()
            if player:
                self.ai.playerID = player.ID
                return 'hunting'
            else:
                return 'exploring'

    def entryActions(self):
        self.ai.turretAngle = self.ai.tankAngle
    def exitAction(self):
        self.ai.resetSpeed()


class AIStateHunting(State):
    def __init__(self,ai):
        State.__init__(self,'hunting')
        self.ai = ai
        self.gotkill = False

    def doActions(self):
        player = self.getClosePlayer()
        if player is None: return
        print '----------------- HUNTING %s ----------------------',player
        distance = self.ai.Vp.get_distance_to(player.Vp) #< 2.0*self.ai.nestsize: #/2:
        print 'distance to player => ',distance
        if distance > 1.5*self.ai.nestsize/2.0:
            self.ai.resetSpeed()
            self.ai.autorotateTank(player)
            self.ai.autotarget(player)
        else:
            self.ai.speed = 0
            self.ai.autorotateTank(player)
            self.ai.fireMG()
        if player.health <= 0:
            self.ai.world.removeEntity(player)
            self.gotkill = True

    def checkCondition(self):
#       if self.ai.IsOutOfNest():  return 'home'
        distance = self.ai.Vp.get_distance_to(self.ai.nestposition) #< 2.0*self.ai.nestsize: #/2:
        # --- ai is far from its nest ----
        if distance > self.ai.nestsize * 2.0:
            return 'home'
        # --- player killed ---
        if self.gotkill:
            return 'exploring'
        # --- player alive ---
        player = self.getClosePlayer()
        if player is None:
            return 'exploring'
        else: # player is out of sight
            return None

    def entryActions(self):
        self.ai.resetSpeed()

    def exitActions(self):
        self.gotkill = False
        self.ai.resetSpeed()
