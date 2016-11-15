''' 020 shooting from tank.py
    demo of 2 tanks shooting bullets at the end of it's cannon
    and shooting tracers at the end of it's bow Machine Gun
    and from the turret-machine gun (co-axial with main gun)
    '''

from Ai import *

fps = 4*60

class Text(pygame.sprite.Sprite):
    number = 0
    book = {}
    def __init__(self,pos,msg):
        self.number = Text.number
        Text.number += 1
        Text.book[self.number] = self
        pygame.sprite.Sprite.__init__(self)
        self.pos = Vector(pos)
        self.newMsg(msg)
        if len(Text.book)>0:
            print Text.number, self.number
            self.kill()
            #del Text.book[self.number-1]
    def update(self,seconds):
        pass
    def newMsg(self,msg,color=black,fontsize=20):
        self.msg = msg
        self.image = write(msg,color,fontsize)
        self.rect = self.image.get_rect()
        self.rect.center = tuple(self.pos)


class World:

    def __init__(self,screen,background):
        self.entities = {}
        self.entityID = 0
        self.screen = screen
        self.background = background

    def create(self):
        # paint a grid of white lines
        screenwidth,screenheight = self.screen.get_size()
        self.screenwidth,self.screenheight = self.screen.get_size()
        self.ainestposition = screenwidth*3/4,screenheight/2
        self.ainestsize =  screenwidth/2
        for x in range(0,screenwidth,screenwidth/xtiles): #start, stop, step
            pygame.draw.line(self.background,gridcolor, (x,0), (x,screenheight))
        for y in range(0,screenheight,screenheight/ytiles): #start, stop, step
            pygame.draw.line(self.background,gridcolor, (0,y), (screenwidth,y))
        # paint upper rectangle to have background for text
        pygame.draw.rect(self.background,lightgray, (0,0,screenwidth, 70))
        pygame.draw.circle(self.background, green,self.ainestposition, self.ainestsize/2)
        pygame.draw.circle(self.background, red,self.ainestposition, 10)
        self.screen.blit(self.background, (0,0)) # delete all


class App:
    def __init__(self):
        self.running = True
        self.onInit()

    def setGroups(self):
        # set sprites group
        self.allgroup = pygame.sprite.LayeredUpdates()
        # set _layer
        Text._layer = 3   # below Tank
        # assign default groups to each sprite class
        Text.groups = self.allgroup

    def initPygame(self):
        # initialize pygame
        pygame.mixer.pre_init(44100,-16,2,2048)
        pygame.init()
        self.screen = pygame.display.set_mode( screensize )
        self.screenrect = self.screen.get_rect()
        self.background = pygame.Surface((self.screen.get_size()))
        self.background.fill(bgcolor) # fill grey light blue:(128,128,255) 
        self.background = self.background.convert()
        self.clock = pygame.time.Clock()    # create pygame clock object

    def onInit(self):
        self.initPygame()
        self.world = World(self.screen,self.background)
        self.world.create()
        self.setGroups()

    def onEvent(self,event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False # exit game
                return
    def render(self,seconds):
        pygame.display.set_caption("FPS: %.2f keys: %s" % ( self.clock.get_fps(), pressedKeysString()))
        self.allgroup.clear(self.screen, self.background) # funny effect if you outcomment this line
        self.writeState()
        self.allgroup.update(seconds)
        self.allgroup.draw(self.screen)
        pygame.display.flip() # flip the screen 30 times a second

    def cleanUp(self):
        pygame.quit()

    def writeState(self):
        import random
        li = ['first item','second item','third item']
        activestate = random.choice(li)
        pos = 10,self.world.screenheight-60
        pos = 300,200
        self.text = Text(pos,activestate)
        self.allgroup.add(self.text)
    
    def mainloop(self):
        while self.running:
            seconds = self.clock.tick(fps)/1000.0 # seconds passed since last frame (float)
            for event in pygame.event.get():
                self.onEvent(event)
            self.render(seconds)
            self.allgroup.remove(self.text)
        self.cleanUp()

if __name__ == '__main__':
    theApp = App()
    theApp.mainloop()
