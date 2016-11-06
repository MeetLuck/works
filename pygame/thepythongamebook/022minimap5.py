''' 020 shooting from tank.py
    demo of 2 tanks shooting bullets at the end of it's cannon
    and shooting tracers at the end of it's bow Machine Gun
    and from the turret-machine gun (co-axial with main gun)
    '''
from Ai import *

class World:

    def __init__(self):
        self.entities = {}
        self.entityID = 0

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

    def getCloseEntity(self,name,location,erange=100):
        # name = entity such as 'leaf','spider'
        # distance = from location to entity location
        print 'get close entity'
        location = Vector2(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < erange:
                    return entity # inside erange
        return None

class App:
    def __init__(self):
        self.running = True
        self.onInit()
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
        Text._layer = 3   # below Tank
        Instruction._layer = 9   # below Tank
        Minimap._layer = 3  # below Tank # better 9 ?
        Fragment._layer = 99
        #assign default groups to each sprite class
        Tank.groups = self.tankgroup, self.allgroup
        Turret.groups = self.allgroup
        CannonBall.groups = self.CannonBallgroup, self.allgroup
        MGBullet.groups = self.MGBulletgroup, self.allgroup
        Fragment.groups = self.allgroup
        Lifebar.groups = self.allgroup
        Text.groups = self.allgroup
        Instruction.groups = self.allgroup
        Minimap.groups = self.allgroup

    def initPygame(self):
        # initialize pygame
        pygame.mixer.pre_init(44100,-16,2,2048)
        pygame.init()
        self.screen = pygame.display.set_mode( screensize )
        self.screenrect = self.screen.get_rect()
        self.background = pygame.Surface((self.screen.get_size()))
        self.background.fill(bgcolor) # fill grey light blue:(128,128,255) 
        self.background = self.background.convert()

        # paint a grid of white lines
        for x in range(0,screenwidth,screenwidth/xtiles): #start, stop, step
            pygame.draw.line(self.background,gridcolor, (x,0), (x,screenheight))
        for y in range(0,screenheight,screenheight/ytiles): #start, stop, step
            pygame.draw.line(self.background,gridcolor, (0,y), (screenwidth,y))
        # paint upper rectangle to have background for text
        pygame.draw.rect(self.background,lightgray, (0,0,screenwidth, 70))
        self.screen.blit(self.background, (0,0)) # delete all
        self.clock = pygame.time.Clock()    # create pygame clock object

    def loadSound(self):
        # ---------- load sound -----------
        folder = 'data'
        self.world.cannonsound = pygame.mixer.Sound(os.path.join(folder,'cannon.ogg'))
        self.world.mg1sound = pygame.mixer.Sound(os.path.join(folder,'mg1.ogg'))
        self.world.mg2sound = pygame.mixer.Sound(os.path.join(folder,'mg2.ogg'))
        self.world.mg3sound = pygame.mixer.Sound(os.path.join(folder,'mg3.ogg'))
        self.world.hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))
        self.world.cannonhitsound = pygame.mixer.Sound(os.path.join(folder,'cannoncrash.ogg'))

    def onInit(self):
        self.world = World()
        self.initPygame()
        self.loadSound()
        self.setGroups()
        self.player = Player(self.world,'player',(150,250), 0) # create  first tank, looking north
        self.ai = AI(self.world,'ai',(450,250), 90) # create second tank, looking south
        self.minimap = Minimap(self)
        status3 = Text((screenwidth//2, 10), "Tank Demo. Press ESC to quit")
        self.instruction = Instruction(self,yellowgreen,32)

    def onEvent(self,event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False # exit game
                return
        if event.type == pygame.KEYDOWN:
            self.instruction.event(event)
            self.minimap.event(event)

    def collision(self):
        #pygame.sprite.spritecollide(sprite, group, dokill, collided = None): return Sprite_list
        for tank in self.tankgroup:
            tank.getCannonhit = False
            tank.getMGhit = False
            cannonhitgroup = pygame.sprite.spritecollide(tank, self.CannonBallgroup, False)
            MGhitgroup = pygame.sprite.spritecollide(tank, self.MGBulletgroup, False)
            for cannonball in cannonhitgroup:
                if cannonball.boss.number != tank.number:
                    print 'gethit tank',cannonball.boss.number, tank.number
                    tank.getCannonhit = True # will get a blue border from Bird.update()
                    cannonball.kill() # remove bullet from all the groups
            for mgbullet in MGhitgroup:
                if mgbullet.boss.number != tank.number:
                    print 'gethit tank',mgbullet.boss.number, tank.number
                    tank.getMGhit = True # will get a blue border from Bird.update()
                    mgbullet.kill() # remove bullet from all the groups

    def render(self,seconds):
        pygame.display.set_caption("FPS: %.2f keys: %s" % ( self.clock.get_fps(), pressedKeysString()))
        self.allgroup.clear(self.screen, self.background) # funny effect if you outcomment this line
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        pygame.display.flip() # flip the screen 30 times a second

    def cleanUp(self):
        pygame.quit()

    def mainloop(self):
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
