''' 020 shooting from tank.py
    '''
from Ai import *
from helper import *


class World:

    def __init__(self,app):
        self.entities = {}
        self.entityID = 0
        self.screen = app.screen
        self.background = app.background
        self.screensize = self.screenwidth,self.screenheight = self.screen.get_size()
        self.nestposition = int(self.screenwidth*2.5/4.0), int(self.screenheight/2.0)
        self.nestsize     = int(self.screenwidth/4.0)
        self.create()

    def addEntity(self,entity):
        self.entities[self.entityID] = entity
        entity.ID = self.entityID
        self.entityID += 1

    def removeEntity(self,entity):
        del self.entities[entity.ID]

    def getEntity(self,entityID):  # get entity using entities[entityID]
        if entityID in self.entities.keys():
            return self.entities[entityID]
        return None

    def getAi(self):
        for entity in self.entities.values():
            if entity.name == 'ai':
                return entity
        return None

    def getPlayer(self):
        for entity in self.entities.values():
            if entity.name == 'player':
                return entity
        return None

    def getCloseEntity(self,name,location,erange=100):
        for entity in self.entities.values():
            if entity.name != name: continue
            distance = location.get_distance_to(entity.Vp)
            if distance < erange:
                return entity # inside erange
        return None

    def create(self):
        self.loadSound()
        # paint a grid of white lines
        self.drawBackground()
        player = Player(self,'player',(150,250), 0) # create  first tank, looking north
        ai     = AI(self,'ai',self.nestposition, 90) # create second tank, looking south
        self.addEntity(player)
        self.addEntity(ai)
        self.minimap = Minimap(self)
        self.status = Status(self)

    def loadSound(self):
        # ---------- load sound -----------
        folder = '../data'
        self.cannonsound = pygame.mixer.Sound(os.path.join(folder,'cannon.ogg'))
        self.mg1sound = pygame.mixer.Sound(os.path.join(folder,'mg1.ogg'))
        self.mg2sound = pygame.mixer.Sound(os.path.join(folder,'mg2.ogg'))
        self.mg3sound = pygame.mixer.Sound(os.path.join(folder,'mg3.ogg'))
        self.hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))
        self.cannonhitsound = pygame.mixer.Sound(os.path.join(folder,'cannoncrash.ogg'))

    def drawBackground(self):
        # paint upper rectangle to have background for text
        pygame.draw.rect(self.background,lightgray, (0,0,self.screenwidth, 70))
        pygame.draw.circle(self.background, lightgreen,self.nestposition, self.nestsize)
        pygame.draw.circle(self.background, red,self.nestposition, 10)
        xtiles,ytiles = 50,50
        for x in range(0,self.screenwidth,self.screenwidth/xtiles): #start, stop, step
            pygame.draw.line(self.background,gridcolor, (x,0), (x,self.screenheight))
        for y in range(0,self.screenheight,self.screenheight/ytiles): #start, stop, step
            pygame.draw.line(self.background,gridcolor, (0,y), (self.screenwidth,y))

        self.screen.blit(self.background, (0,0)) # delete all

class App:
    def __init__(self):
        self.running = True
        self.onInit()

    def initPygame(self):
        pygame.mixer.pre_init(44100,-16,2,2048)
        pygame.init()
        self.screensize = 1024,768
        self.screen = pygame.display.set_mode( self.screensize )
        self.background = pygame.Surface((self.screen.get_size()))
        self.background.fill(bgcolor) # fill grey light blue:(128,128,255) 
        self.background = self.background.convert()
        self.clock = pygame.time.Clock()    # create pygame clock object

    def onInit(self):
        self.initPygame()
        self.setGroups()
        self.world = World(self)

    def setGroups(self):
        # set sprites group
        self.tankgroup = pygame.sprite.Group()
        self.CannonBallgroup = pygame.sprite.Group()
        self.MGBulletgroup = pygame.sprite.Group()
        self.allgroup = pygame.sprite.LayeredUpdates()
        # set _layer
        Tank._layer = 4   # base layer
        Turret._layer = 6 # above Tank & Tracer
        CannonBall._layer = 7 # to prove that Bullet is in top-layer
        MGBullet._layer = 7 # to prove that Bullet is in top-layer
        Text._layer = 99   # below Tank
        Status._layer = 99   # below Tank
        Minimap._layer = 3  # below Tank # better 9 ?
        Fragment._layer = 99
        # assign default groups to each sprite class
        Tank.groups = self.tankgroup, self.allgroup
        Turret.groups = self.allgroup
        CannonBall.groups = self.CannonBallgroup, self.allgroup
        MGBullet.groups = self.MGBulletgroup, self.allgroup
        Fragment.groups = self.allgroup
        Lifebar.groups = self.allgroup
        Text.groups = self.allgroup
        Status.groups = self.allgroup
        Minimap.groups = self.allgroup

    def onEvent(self,event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False # exit game
                return
        if event.type == pygame.KEYDOWN:
            self.world.minimap.event(event)

    def render(self,seconds):
        pygame.display.set_caption("FPS: %.2f keys: %s" % ( self.clock.get_fps(), pressedKeysString()))
        self.allgroup.clear(self.screen, self.background) # funny effect if you outcomment this line
        self.updateState()
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        pygame.display.flip() # flip the screen 30 times a second

    def collision(self):
        #pygame.sprite.spritecollide(sprite, group, dokill, collided = None): return Sprite_list
        for tank in self.tankgroup:
            tank.getCannonhit = False
            tank.getMGhit = False
            cannonhitgroup = pygame.sprite.spritecollide(tank, self.CannonBallgroup, False)
            MGhitgroup = pygame.sprite.spritecollide(tank, self.MGBulletgroup, False)
            for cannonball in cannonhitgroup:
                if cannonball.boss.number != tank.number:
                    #print 'gethit tank',cannonball.boss.number, tank.number
                    tank.getCannonhit = True # will get a blue border from Bird.update()
                    cannonball.kill() # remove bullet from all the groups
            for mgbullet in MGhitgroup:
                if mgbullet.boss.number != tank.number:
                    #print 'gethit tank',mgbullet.boss.number, tank.number
                    tank.getMGhit = True # will get a blue border from Bird.update()
                    mgbullet.kill() # remove bullet from all the groups

    def render(self,seconds):
        self.allgroup.clear(self.screen, self.background) # funny effect if you outcomment this line
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        pygame.display.flip() # flip the screen 30 times a second

    def cleanUp(self):
        pygame.quit()

    def mainloop(self):
        fps = 60
        while self.running:
            seconds = self.clock.tick(fps)/1000.0 # seconds passed since last frame (float)
            for event in pygame.event.get():
                self.onEvent(event)
            self.collision()
            self.render(seconds)
        self.cleanUp()

if __name__ == '__main__':
    theApp = App()
    theApp.mainloop()
