from class79 import *
#from 79Class import *

class World(object):

    def __init__(self,background):
        self.entities = {}
        self.entityID = 0
        self.background = background

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
        self.OnInit()
        self.world = World(self.background)
        self.running = True
        for antNum in range(ANTCOUNT): # make ant object
            ant = Ant(self.world,self.antimage)
            ant.location = Vector2( randint(0,screenwidth),randint(0,screenheight))
            self.world.addEntity(ant)

    def initPygame(self):
        pygame.init()
        self.screen     = pygame.display.set_mode(screensize,0,32)
        self.background = pygame.Surface(screensize)
        self.background.fill(bgcolor)
        self.background = self.background.convert()
        self.drawNest()
        self.screen.blit(self.background,(0,0))
        self.antimage   = pygame.image.load('ant.png').convert_alpha()
        self.leafimage  = pygame.image.load('leaf.png').convert_alpha()
        self.spiderimage = pygame.image.load('spider.png').convert_alpha()
        self.clock = pygame.time.Clock()
        self.fps = 60
    def drawNest(self):
        pygame.draw.circle(self.background, nestcolor, nestposition, int(nestsize))

    def setGroups(self):
        # set sprites group
        self.antgroup = pygame.sprite.Group()
        self.leafgroup = pygame.sprite.Group()
        self.spidergroup = pygame.sprite.Group()
        self.allgroup = pygame.sprite.LayeredUpdates()
        # set _layer
        Ant._layer      = 4 
        Leaf._layer     = 4
        Spider._layer   = 4
        #assign default groups to each sprite class
        Ant.groups      = self.antgroup,    self.allgroup
        Leaf.groups     = self.leafgroup,   self.allgroup
        Spider.groups   = self.spidergroup, self.allgroup

    def OnInit(self):
        self.initPygame()
        self.setGroups()

    def onEvent(self,event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False # exit game
    def render(self,seconds):
        pygame.display.set_caption("FPS: %.2f " % self.clock.get_fps() )
        self.allgroup.clear(self.screen, self.background) # funny effect if you outcomment this line
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        pygame.display.flip() # flip the screen 30 times a second

    def cleanUp(self):
        pygame.quit()

    def mainloop(self):

        while self.running:
            for event in pygame.event.get():
                self.onEvent(event)
            if randint(1,100) == 1: # 1/50 -> make Leaf in the 2% chance
                leaf = Leaf(self.world,self.leafimage)
                leaf.location = Vector2(randint(0,screenwidth-1),randint(0,screenheight-1))
                self.world.addEntity(leaf)  # add leaf to the world
            if randint(1,200) == 1:   # 5/1000  -> make spider in the 0.5% chance
                spider = Spider(self.world, self.spiderimage)
                spider.location = Vector2( -50, randint(0,screenheight) )
                spider.destination = Vector2(screenwidth+50, randint(0, screenheight) )
                self.world.addEntity(spider)  # add spider to the world

            seconds = self.clock.tick(self.fps)/1000.0
            self.render(seconds)
        self.cleanUp()

if __name__ ==  '__main__':
    app = App()
    app.mainloop()
