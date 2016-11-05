from class79 import *
#from 79Class import *

class World(object):

    def __init__(self,screen):
        self.entities = {}
        self.entityID = 0
        self.bgsurf = pygame.surface.Surface(screen.get_size()).convert()
        self.bgsurf.fill(white)
        # draw nest
        pygame.draw.circle(self.bgsurf, nestcolor, nestposition, int(nestsize))

    def addEntity(self,entity):
        self.entities[self.entityID] = entity
        entity.ID = self.entityID
        self.entityID += 1

    def removeEntity(self,entity):
        del self.entities[entity.ID]

    def get(self,entityID):  # get entity using entities[entityID]
        if entityID in self.entities.keys():
            return self.entities[entityID]
        return None

    def process(self,timepassed):
        for entity in self.entities.values():
            entity.process(timepassed)

    def render(self,surface):
        surface.blit(self.bgsurf,(0,0))
        for entity in self.entities.values():
            entity.render(surface)

    def getCloseEntity(self,name,location,erange=100):
        # name = entity such as 'leaf','spider'
        # distance = from location to entity location
        location = Vector2(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < erange:
                    return entity # inside erange
        return None


class App:

    def __init__(self):
        # make world
        self.initPygame()
        self.world = World(self.screen)
        self.running = True
        for antNum in range(ANTCOUNT):
            # make ant object
            ant = Ant(self.world,self.antimage)
            ant.location = Vector2( randint(0,screenwidth),randint(0,screenheight))
            # set ant's State as Exploring
            ant.brain.setState('exploring')
            # add ant to the world
            self.world.addEntity(ant)
    def initPygame(self):
        # initialize pygame
        pygame.init()
        self.screensize = self.screenwidth,self.screenheight = 640,480
        self.screen     = pygame.display.set_mode(self.screensize,0,32)
        self.antimage   = pygame.image.load('ant.png').convert_alpha()
        self.leafimage  = pygame.image.load('leaf.png').convert_alpha()
        self.spiderimage = pygame.image.load('spider.png').convert_alpha()
        self.clock = pygame.time.Clock()
        self.fps = 60

    def onEvent(self,event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False # exit game

    def cleanUp(self):
        pygame.quit()

    def mainloop(self):

        while self.running:
            for event in pygame.event.get():
                self.onEvent(event)
            if randint(1,50) == 1: # 1/50 -> make Leaf in the 2% chance
                leaf = Leaf(self.world,self.leafimage)
                leaf.location = Vector2(randint(0,self.screenwidth-1),randint(0,self.screenheight-1))
                self.world.addEntity(leaf)  # add leaf to the world
            if randint(1,200) == 1:   # 5/1000  -> make spider in the 0.5% chance
                spider = Spider(self.world, self.spiderimage)
                spider.location = Vector2( -50, randint(0,self.screenheight) )
                spider.destination = Vector2(self.screenwidth+50, randint(0, self.screenheight) )
                self.world.addEntity(spider)  # add spider to the world

            timepassed = self.clock.tick(self.fps)/1000.0
            # process all entities in the world
            # entity.process(timepassed)
            self.world.process(timepassed)
            # draw world
            self.world.render(self.screen)
            # update display
            pygame.display.update()
        self.cleanUp()

if __name__ ==  '__main__':
    app = App()
    app.mainloop()
