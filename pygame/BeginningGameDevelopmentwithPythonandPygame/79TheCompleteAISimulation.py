import pygame
from pygame.locals import *
from random import randint,choice
from gameobjects.vector2 import Vector2

screensize = 640,480
nestposition = 320,240
antcount = 20
netsize = 100

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

class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.activestate = None
    def addState(self,state):
        self.states[state.name] = state
    def think(self):
        if self.activestate is None : return
        self.activestate.doActions()
        newstate_name = self.activestate.checkCoditions()
        if newstate_name is not None:
            self.setState(newstate_name)
    def setState(self,newstate_name):
        if self.activestate is not None:
            self.activestate.exitActions()
        self.activestate = self.states[newstate_name]
        self.activestate.entryActions()
class World(object):
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        self.bgsurf = pygame.surface.Surface(screensize).convert()
        self.bgsurf.fill(white)
        pygame.draw.circle(self.bgsurf,(200,250,200),nestposition, int(nestsize))
    def addEntity(self,entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
    def removeEntity(self,entity):
        del self.entities[entity.id]
    def get(self,entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
    def process(self,timepassed):
        for entity in self.entities.values():
            entity.process(timepassed)
    def render(self,surface):
        surface.blit(self.bgsurf,(0,0))
        for entity in self.entities.values():
            entity.render(surface)
    def getCloseEntity(self,name,location,erange=100):
        location = Vector2(*location)
        for entity in elf.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < erange:
                    return entity
        return None

class GameEntity(object):
    def __init__(self,world,name,image):
        self.world = world
        self.name = name
        self.location = Vector2(0,0)
        self.destination = Vector2(0,0)
        self.speed = 0
        self.brain = StateMachine()
        self.id = 0
    def render(self,surface):
        x,y = self.location
        w,h = self.image.get_size()
        surface.blit(self.image, (x-w/2,y-h/2) )
    def process(self,timepassed):
        self.brank.think()
        if self.speed > 0 and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            dist_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(dist_to_destination, self.speed * timepassed)
            self.location += travel_distance * heading

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
            self.speed = 0
            self.image = self.deadimage
        self.speed = 140
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
        if x > screewidth + 2:
            self.world.removeEntity(self)
            return
        GameEntity.process(self,timepassed)

class Ant(GameEntity):
    def __init__(self,world,image):
        GameEntity.__init__(self,world,'ant',image)
        exploringstate = AntStateExploring(self)
        seekingstate = AntStateSeeking(self)
        deliveringstate = AntStateDelivering(self)
        huntingstate = AntStateHunting(self)

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
    def __init__(self,ant):
        State.__init__(self,'exploring')
        self.ant = ant
    def randomDestination(self):
        self.ant.destination = Vector2( randint(0,screenwidth), randint(0,screenehgiht))
    def doActions(self):
        if randint(1,20) == 1:
            self.randomDestination()
    def checkConditions(self):
        leaf = self.ant.world.getCloseEntity('leaf',self.ant.location)
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return 'seeking'
        spider = self.ant.world.getCloseEntity('spider',nestposition,nestsize)
        if spider is not None:
            if self.ant.location.get_distance_to(spider.location) < 100:
                self.ant.spider_id = spider.id
                return 'hunting'
        return None
    def entryActions(self):
        self.ant.speed = 120 + randint(-30,30)
        self.randomDestination()

class AntStateSeeking(State):
    def __init__(self,ant):
        State.__init__(self,'seeking')
        self.ant = ant
        self.leaf_id = None
    def checkConditions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is None:
            return 'exploring'
        if self.ant.location.get_distance_to(leaf.location) < 5:
            self.ant.carry(leaf.image)
            self.ant.world.removeEntity(leaf)
            return 'delivering'
        return None
    def entryActions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is not None:
            self.ant.destination = leaf.location
            self.ant.speed = 160 + randinit(-20,20)

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

def run():
    pygame.init()
    screen = pygame.display.set_mode(screensize,0,32)
    world = World()
    w,h = screensize
    clock = pygame.time.Clock()
    antimage = pygame.image.load('ant.png').conver_alpha()
    leafimage = pygame.image.load('leaf.png').conver_alpha()
    spiderimage = pygame.image.load('spider.png').conver_alpha()
    for antno in range(antcount):
        ant = Ant(world,antimage)
        ant.location = Vector2( randint(o,screenwidth),randint(0,screenheight))
        ant.brain.setState('exploring')
        world.addEntity(ant)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit(); exit()
        timepassed = clock.tick(fps)/1000.0
        if randint(1,10) == 1:
            leaf = Leaf(world,leafimage)
            leaf.location = Vector2(randint(0,screenwidth),randint(0,screenheight))
            world.addEntity(leaf)
        if randint(1,100) == 1:
            spider = Spider(world, spiderimage)
            spider.location = Vector2( -50, randint(0,screenheight) )
            spider.destination = Vector2(screenwidth+50, randint(0, screenheight) )
            world.addEntity(spider)
        world.process(timepassed)
        world.render(screen)
        pygame.display.update()

if __name__ ==  '__main__':
    run()
