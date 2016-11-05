import pygame
from pygame.locals import *
from random import randint,choice
from gameobjects.vector2 import Vector2

# constants
screensize = screenwidth,screenheight = 640,480
fps = 60
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')
nestposition = 320,240
nestsize = 100
nestcolor = (200,250,200)
ANTCOUNT = 20

class State(object): # Exploring, Seeking, Hunting
    def __init__(self,name):
        self.name = name
    def doActions(self):
        pass
    def checkConditions(self):
        pass
    def entryActions(self):  # called when entering new-state
        pass
    def exitActions(self):   # called when exiting current-state
        pass

class StateMachine(object): # brain

    def __init__(self):
        self.states = {}
        self.activestate = None

    def addState(self,state):
       " add state such as exploring,seeking,hunting "
       self.states[state.name] = state

    def think(self):  # change State according to conditions
        if not self.activestate: return
        # --- active state starts ---
        self.activestate.doActions()
        # for exploring state -> go random dest
        newstate = self.activestate.checkConditions()
        # exploring, seeking a leaf, delivering a leaf, hunting a spider
        if newstate:
            self.setState(newstate)

    def setState(self,newstate):
        if self.activestate:
            self.activestate.exitActions() # run when exiting current state
        self.activestate = self.states[newstate]
        self.activestate.entryActions()    # run when entering new state

class GameEntity(object):
    # such as 'leaf','ant','spider'
    def __init__(self,world,name,image):
        self.world = world
        self.name  = name
        self.ID = 0
        self.image = image
        self.speed = 0
        self.location    = Vector2(0,0)
        self.destination = Vector2(0,0)
        # brain
        self.brain = StateMachine()

    def render(self,surface):
        x,y = self.location
        w,h = self.image.get_size()
        surface.blit(self.image, (x-w/2,y-h/2) )

    def process(self,timepassed):
        # 1. change State
        # 2. move entity according to the entity's State
        self.brain.think() # state machine.think()
        # change State such as Exploring,Seeking,Delivering,Hunting
        self.move(timepassed)

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
        GameEntity.__init__(self,world,'leaf',image)

class Spider(GameEntity):

    def __init__(self,world,image):
        GameEntity.__init__(self,world,'spider',image)
        self.deadimage = pygame.transform.flip(image,0,1)
        self.health = 25
        self.speed = 50 + randint(-20,20)

    def bitten(self):
        self.health -= 1
        if self.health <= 0:
            self.speed = 0 # stop
            self.image = self.deadimage
        self.speed = 140   # runaway

    def render(self,surface):
        GameEntity.render(self,surface)
        x,y = self.location
        w,h = self.image.get_size()
        barX = x - 12
        barY = y + h/2
        surface.fill( red,  (barX,barY,25,4) )
        surface.fill( green,(barX,barY,self.health,4) )

    def process(self,timepassed):
        x,y = self.location
        if x > screenwidth + 2:
            self.world.removeEntity(self)
            return
        GameEntity.process(self,timepassed)

class Ant(GameEntity):

    def __init__(self,world,image):
        # call base Class __init__
        GameEntity.__init__(self,world,'ant',image)
        # define states
        exploringstate = AntStateExploring(self)   # self = Ant object
        seekingstate = AntStateSeeking(self)
        deliveringstate = AntStateDelivering(self)
        huntingstate = AntStateHunting(self)
        # self.bain = StateMachin() from GameEntity(base class)
        self.brain.addState(exploringstate)
        self.brain.addState(seekingstate)
        self.brain.addState(deliveringstate)
        self.brain.addState(huntingstate)

        self.carryimage = None

    def carry(self,image):
        self.carryimage = image

    def drop(self,surface):
        if self.carryimage:
            x,y = self.location
            w,h = self.carryimage.get_size()
            surface.blit(self.carryimage, (x-w,y-h/2))
            self.carryimage = None

    def render(self,surface):
        GameEntity.render(self,surface)
        if self.carryimage:
            x,y = self.location
            w,h = self.carryimage.get_size()
            surface.blit(self.carryimage, (x-w,y-h/2))

class AntStateExploring(State):
    # Exploring State -> leaf   -> Seeking State
    # Exploring State -> spider -> Hunting State
    def __init__(self,ant):
        State.__init__(self,'exploring')
        # self.name = 'exploring' by calling State constructor
        self.ant = ant

    def randomDestination(self):
        self.ant.destination = Vector2( randint(0,screenwidth), randint(0,screenheight))

    def doActions(self):
        if randint(1,20) == 1: # 5% chance of radom destination
            self.randomDestination()

    def foundLeaf(self):
        leaf = self.ant.world.getCloseEntity('leaf',self.ant.location)
        if leaf: # if leaf is not None:
            self.ant.leaf_id = leaf.ID
            return True

    def foundSpider(self):
        spider = self.ant.world.getCloseEntity('spider',nestposition,nestsize)
        if spider: # if spider is not None:
            if self.ant.location.get_distance_to(spider.location) < 100:
                self.ant.spider_id = spider.ID
                return True

    def checkConditions(self):
        if self.foundLeaf(): return 'seeking'
        if self.foundSpider(): return 'hunting'
        return None

    def entryActions(self):   # when entering Exploring State from other State
        self.ant.speed = 120 + randint(-30,30)
        self.randomDestination()

class AntStateSeeking(State):

    def __init__(self,ant):
        State.__init__(self,'seeking')
        self.ant = ant
        self.leaf_id = None

    def checkConditions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if not leaf:  # if no leaf, change State to Exploring
            return 'exploring'
        if self.ant.location.get_distance_to(leaf.location) < 5:
            # if found leaf and in the range of 5 pixel
            # change State to Delivering
            self.ant.carry(leaf.image)
            # re
            self.ant.world.removeEntity(leaf)
            return 'delivering'
        return None

    def entryActions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf: 
            self.ant.destination = leaf.location
            self.ant.speed = 160 + randint(-20,20)

class AntStateDelivering(State):
    def __init__(self,ant):
        State.__init__(self,'delivering')
        self.ant = ant
    def checkConditions(self):
        if Vector2(*nestposition).get_distance_to(self.ant.location) < nestsize:
            if randint(1,10) == 1:
                self.ant.drop(self.ant.world.bgsurf)
                return 'exploring'
        return None
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
        spider = self.ant.world.get(self.ant.spider_id)
        if spider is None: return None
        # --- found spider ---
        self.ant.destination = spider.location
        if self.ant.location.get_distance_to(spider.location) < 15:
            if randint(1,5) == 1:
                spider.bitten()
                if spider.health <= 0:
                    self.ant.carry(spider.image)
                    self.ant.world.removeEntity(spider)
                    self.got_kill = True
    def checkConditions(self):
        if self.got_kill:
            return 'delivering'
        spider = self.ant.world.get(self.ant.spider_id)
        if spider is None: return 'exploring'
        if spider.location.get_distance_to(nestposition) > 3 * nestsize:
            return 'exploring'
        return None
    def entryActions(self):
        self.speed = 160 + randint(0,50)
    def exitActions(self):
        self.got_kill = False
