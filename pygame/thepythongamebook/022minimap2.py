''' 020 shooting from tank.py
    demo of 2 tanks shooting bullets at the end of it's cannon
    and shooting tracers at the end of it's bow Machine Gun
    and from the turret-machine gun (co-axial with main gun)
    '''
from Entity import *

class World:
    def __init__(self):
        self.running = True
        self.onInit()

    def setGroups(self):
        # set sprites group
        self.tankgroup = pygame.sprite.Group()
        self.bulletgroup = pygame.sprite.Group()
        self.allgroup = pygame.sprite.LayeredUpdates()
        # set _layer
        Tank._layer = 4   # base layer
        Turret._layer = 6 # above Tank & Tracer
        Bullet._layer = 7 # to prove that Bullet is in top-layer
        Text._layer = 3   # below Tank
        Instruction._layer = 9   # below Tank
        Minimap._layer = 3  # below Tank # better 9 ?
        #assign default groups to each sprite class
        Tank.groups = self.tankgroup, self.allgroup
        Turret.groups = self.allgroup
        Bullet.groups = self.bulletgroup, self.allgroup
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
        self.cannonsound = pygame.mixer.Sound(os.path.join(folder,'cannon.ogg'))
        self.mg1sound = pygame.mixer.Sound(os.path.join(folder,'mg1.ogg'))
        self.mg2sound = pygame.mixer.Sound(os.path.join(folder,'mg2.ogg'))
        self.mg3sound = pygame.mixer.Sound(os.path.join(folder,'mg3.ogg'))
        self.hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))
        #hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))

    def onInit(self):
        self.initPygame()
        self.loadSound()
        self.setGroups()
        self.player1 = Tank(self,(150,250), 90) # create  first tank, looking north
        self.player2 = Tank(self,(450,250), 90) # create second tank, looking south
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
            tank.gethit = False
            hitgroup = pygame.sprite.spritecollide(tank, self.bulletgroup, False) #, pygame.sprite.collide_circle)
            # pygame.sprite.collide_circle works only if one sprite has self.radius
            # you can do without that argument collided and only the self.rects will be checked
            for bullet in hitgroup:
                if bullet.boss.number != tank.number:
                    print 'crash tank',bullet.boss.number
                    bullet.boss.gethit = True # will get a blue border from Bird.update()
                    bullet.kill()
                    #crashbird.kill()   # this would remove him from all his groups

    def render(self,seconds):
        pygame.display.set_caption("FPS: %.2f keys: %s" % ( self.clock.get_fps(), pressedKeysString()))
        msg =  "player%i: ammo: %i/%i" % (self.player1.number+1, self.player1.ammo, self.player1.MGammo)
        Text.book[self.player1.number].newMsg(msg)
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
    theWorld = World()
    theWorld.mainloop()
