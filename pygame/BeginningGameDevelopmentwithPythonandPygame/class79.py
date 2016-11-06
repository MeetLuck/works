import pygame
from pygame.locals import *
from random import randint,choice
from gameobjects.vector2 import Vector2
from colors import *

# constants
screensize = screenwidth,screenheight = 640,480
bgcolor = pygame.Color('gray')
nestposition = 320,240
nestsize = 100
nestcolor = (200,250,200)
ANTCOUNT = 10 #20

class State(object): # Exploring, Seeking, Hunting
    def __init__(self,name):
        self.name = name
    def doActions(self):    pass
    def checkCondition(self):  pass
    def entryActions(self): pass
    def exitActions(self):  pass

class Brain(object): # brain

    def __init__(self):
        self.states = {}
        self.activestate = None

    def addState(self,state):
       " add state such as exploring,seeking,hunting "
       self.states[state.name] = state

    def think(self):  # change State according to conditions
        if not self.activestate: return # for spider, leaf
        # --- active state starts ---
        self.activestate.doActions()
        # for exploring state -> go random dest
        newstate = self.activestate.checkCondition()
        # exploring, seeking a leaf, delivering a leaf, hunting a spider
        if newstate:
            self.setActiveState(newstate)

    def setActiveState(self,newstate):
        # exitAction(currentstate) => set activestate => entryAction(newstate)
        if self.activestate:
            self.activestate.exitActions() # run when exiting current state
        self.activestate = self.states[newstate]
        self.activestate.entryActions()    # run when entering new state

class GameEntity(pygame.sprite.Sprite):
    # such as 'leaf','ant','spider'
    def __init__(self,world,name,image,groups):
        pygame.sprite.Sprite.__init__(self,groups)
        #super(GameEntity,self).__init__(groups)
        self.world = world
        self.name  = name
        self.ID = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 0
        self.location    = Vector2(0,0)
        self.destination = Vector2(0,0)
        # brain
        self.brain = Brain()

    def setCenter(self):
        x,y = self.location
        w,h = self.image.get_size()
        self.rect.center = x-w/2,y-h/2

    def update(self,timepassed):
        # 1. change State
        # 2. move entity according to the entity's State
        self.brain.think() # state machine.think()
        # change State such as Exploring,Seeking,Delivering,Hunting
        self.move(timepassed)
        self.setCenter()

    def move(self,timepassed):
        if self.speed <= 0 or self.location == self.destination: return
        # --- move Entity ---
        # difference between destination and location Vectors
        difference = self.destination - self.location
        # get magnitude 
        distance = difference.get_length()
        # get direction => heading
        direction = difference.get_normalized()
        #travel_distance = min(distance, self.speed * timepassed)
        self.location += direction * self.speed * timepassed
        #self.location += travel_distance * direction

class Leaf(GameEntity):
    def __init__(self,world,image):
        GameEntity.__init__(self,world,'leaf',image,self.groups)
    def update(self,timepassed):
        self.setCenter()
        #print 'Leaf update',self.ID,self.rect.center

class Lifebar(GameEntity):
    def draw(self,surface):
        x,y = self.location
        w,h = self.image.get_size()
        barX = x - 12
        barY = y + h/2
        pygame.draw.rect(surface,red, (barX,barY,25,4) ) 
        pygame.draw.rect(surface,green, (barX,barY,self.health,4) )


class Spider(GameEntity):

    def __init__(self,world,image):
        GameEntity.__init__(self,world,'spider',image,self.groups)
        self.deadimage = pygame.transform.flip(image,0,1)
        self.health = 25
        self.speed = 50 + randint(-20,20)

    def bitten(self):
        self.health -= 1
        if self.health <= 0:
            self.speed = 0 # stop
            self.image = self.deadimage
        else:
            self.speed = 140   # runaway

    def update(self,timepassed):
        x,y = self.location
        if x > screenwidth:
            self.world.removeEntity(self)
            self.kill() # remove from sprite groups
            return
        GameEntity.update(self,timepassed)


class Ant(GameEntity):

    def __init__(self,world,image):
        # call base Class __init__
        GameEntity.__init__(self,world,'ant',image,self.groups)
        self.world = world
        # define states
        exploringstate = AntStateExploring(self)   # self = Ant object
        seekingstate = AntStateSeeking(self)
        deliveringstate = AntStateDelivering(self)
        huntingstate = AntStateHunting(self)
        # add State to brain
        self.brain.addState(exploringstate)
        self.brain.addState(seekingstate)
        self.brain.addState(deliveringstate)
        self.brain.addState(huntingstate)
        # carry entity
        self.carryentity = None
        # set ant's State as Exploring
        self.brain.setActiveState('exploring')

    def carry(self,entity):
        self.carryentity = entity

    def drop(self):
        if self.carryentity:
            self.carryentity.location = self.location[:] 
            self.carryentity = None

    def update(self,seconds):
        GameEntity.update(self,seconds)
        if self.carryentity:
            self.carryentity.location = self.location[:]

class AntStateExploring(State):
    # Exploring State -> found leaf   -> change state to Seeking State
    # Exploring State -> found spider -> change state to Hunting State
    def __init__(self,ant):
        State.__init__(self,'exploring') # self.name = 'exploring' by calling State constructor
        self.ant = ant

    def doActions(self):
        if randint(1,20) == 1: # 5% chance of random destination
            self.randomDestination()

    def checkCondition(self):
        if self.foundLeaf():      return 'seeking'
        elif self.foundSpider():  return 'hunting'
        else:                     return  None

    def entryActions(self):   # when entering Exploring State from other State
        self.ant.speed = 120 + randint(-30,30)
        self.randomDestination()

    def randomDestination(self):
        self.ant.destination = Vector2( randint(0,screenwidth), randint(0,screenheight))

    def foundLeaf(self):
        leaf = self.ant.world.getCloseEntity('leaf',self.ant.location)
        if leaf:
            self.ant.leafID = leaf.ID
            return True

    def foundSpider(self):
        spider = self.ant.world.getCloseEntity('spider',nestposition,nestsize)
        if spider and self.ant.location.get_distance_to(spider.location) < 100:
            self.ant.spiderID = spider.ID
            return True

class AntStateSeeking(State):

    def __init__(self,ant):
        State.__init__(self,'seeking')
        self.ant = ant
        self.leafID = None

    def checkCondition(self):
        leaf = self.ant.world.get(self.ant.leafID)
        if not leaf:
            return 'exploring'
        elif leaf and self.ant.location.get_distance_to(leaf.location) < 5:
        # if found leaf and in the range of 5 pixel, change State to Delivering
            self.ant.carry(leaf)
            self.ant.world.removeEntity(leaf)
            return 'delivering'
        else: # leaf is too far, do not change state
            return None

    def entryActions(self): # from exploring state
        leaf = self.ant.world.get(self.ant.leafID)
        if leaf: 
            self.ant.destination = leaf.location
            self.ant.speed = 160 + randint(-20,20)

class AntStateDelivering(State):
    def __init__(self,ant):
        State.__init__(self,'delivering')
        self.ant = ant

    def checkCondition(self):
        if Vector2(*nestposition).get_distance_to(self.ant.location) < nestsize-10:
            if randint(1,10) == 1:
                self.ant.drop()
                return 'exploring'
        return None   # do not change state

    def entryActions(self):
        self.ant.speed = 60
        random_offset = Vector2(randint(-20,20),randint(-20,20))
        self.ant.destination = Vector2(*nestposition) + random_offset

class AntStateHunting(State):
    def __init__(self,ant):
        State.__init__(self,'hunting')
        self.ant = ant
        self.got_kill = False

    def doActions(self):
        spider = self.ant.world.get(self.ant.spiderID)
        if spider is None: return None
        # --- found spider ---
        self.ant.destination = spider.location
        if self.ant.location.get_distance_to(spider.location) < 15:
            if randint(1,5) == 1:
                spider.bitten()
                if spider.health <= 0:
                    self.ant.carry(spider)
                    self.ant.world.removeEntity(spider)
                    self.got_kill = True

    def checkCondition(self): # <-- from hunting state
        if self.got_kill:
            return 'delivering'
        # spider is alive
        spider = self.ant.world.get(self.ant.spiderID)
        if spider is None: return 'exploring'
        if spider.location.get_distance_to(nestposition) > 2 * nestsize:
            return 'exploring'
        return None

    def entryActions(self):
        self.speed = 160 + randint(0,50)

    def exitActions(self):
        self.got_kill = False
