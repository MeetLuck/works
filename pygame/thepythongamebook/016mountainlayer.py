# 016 layers.py
# pygame sprites with different layers and parallax scrolling
# change the sprite layer by clicking with left or right mouse button
# the birdsprites will apear before or behind the blocks
# POINT ON a sprite and press 'p' to print out more information about that  sprite
from constants016 import *

class Text(pygame.sprite.Sprite):
    def __init__(self,msg):
        self.groups = textgroup, allgroup
        self._layer = 99
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.newMsg(msg)
    def update(self,time):
        pass
    def newMsg(self, msg ='i have nothing to say'):
        self.image = write(msg)
        self.rect = self.image.get_rect()
        self.rect.center = screenwidth/2, 10

class Mountain(pygame.sprite.Sprite):
    # generate a mountain sprite for the background to demonstrate parallax scrolling
    # like in the classic 'moonbuggy' game. Mountains slide from right to left
    # self.centerx, self.centery => self.rect.center
    def __init__(self,atype):
        # assign self._layer BEFORE calling pygame.sprite.Sprite.__init__
        self.type = atype
        self.set_layer()
        self.groups = mountaingroup, allgroup
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.dy = 0.0
        width = 1.5 * 100 * self.type # 1.5%
        height = screenheight/2.0 + 50.0*(self.type-1)
        self.image = pygame.Surface( (width,height)) #self.image.fill(green)
        self.image.set_colorkey(black)
        pygame.draw.polygon(self.image, self.color,
              ( (0,height),
                (0,height-10*self.type),
                (width/2, int( random.random() * height/2.0 ) ),
                (width,height),
                (9,height) ), 0)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        # x,y -> self.image.get_rect().center
        self.centerx = screenwidth  + self.rect.width/2.0
        self.centery = screenheight - self.rect.height/2.0
        # SET center = self.center = self.centerx,self.centery
        self.rect.center = self.center
        self.insideScreen = False
    def set_layer(self):
        if self.type == 1:
            self._layer = -1  # blue Mountain
            self.dx = -100.0
            self.color = blue
        elif self.type == 2:  # pink Mountain
            self._layer = -2
            self.dx = -75.0
            self.color = pink
        else:
            self._layer = -3  # red Mountain
            self.dx = -35.0
            self.color = red

    @property
    def center(self):
        return self.centerx, self.centery

    def move(self,time):
        self.centerx += self.dx * time
        self.centery += self.dy * time
        # set center
        self.rect.center = self.center
    def isInsideScreen(self):
        return self.rect.centerx < screenwidth

    def update(self,time):
        self.move(time)
        # kill mountains too far to the left
        if self.rect.right < 0:  # right = self.rect.centerx + self.rect.width/2
            self.kill()
        # create new mountains if necessary
        if self.insideScreen:
            return
        # coming from outside Screen
        if self.isInsideScreen():       # check if self.rect.centerx is Inside screen
            Mountain(self.type)         # create a new Mountain coming from the right side
            self.insideScreen = True    # no more than one Moutain at a time

class BirdCatcher(pygame.sprite.Sprite):
    # circle around the mouse pointer. 
    # LEFT button create new sprite, RIGHT button kill sprite
    def __init__(self):
        self._layer = 9
        self.groups = catchergroup, allgroup
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (100,100) )
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 50
        pygame.draw.circle(self.image,red,(self.radius,self.radius), self.radius, 2)
    def update(self,seconds):
        self.rect.center = pygame.mouse.get_pos()


#--- define sprite Group before creating sprites
#blockgroup = pygame.sprite.LayeredUpdates()
textgroup = pygame.sprite.Group()
catchergroup = pygame.sprite.Group()
mountaingroup = pygame.sprite.Group()

# only allgroup draws the sprite, so use LayeredUpdates() instead Group()
allgroup = pygame.sprite.LayeredUpdates() # can draw sprites in layers

'''
>>> When using 'pygame.sprite.Layeredupdate()' instead of 'pygame.sprite.Group()',
>>> you can give each sprite a variable 'self._layer' as well as a variable groups
>>> to influence 'the drawing order of the sprite'.

The sprite groups must exist (be defined in the mainloop) before you can assign sprites to the groups.
>>> Inside the class, you must assign groups and '_layer' 
>>> BEFORE you call 'pygame.sprite.Sprite.__init__(self, *groups)'
'''

def main():
    # draw background
    bgsurf = pygame.Surface( screensize )
    bgsurf.fill(white)
    bgsurf.blit(write("press left mouse button to increase Bird's layer"),(50,40))
    bgsurf.blit(write("press right mouse button to decrease Bird's layer."),(50,65))
    bgsurf.blit(write("layer of mountains are: -1 (blue), -2 (pink), -3 (red)"),(50,90))
    bgsurf.blit(write("Press ESC to quit, p to print info at mousepos"), (50,115))
    bgsurf = bgsurf.convert_alpha()
    screen.blit(bgsurf,(0,0) )

    #--- load sound
    crysound = pygame.mixer.Sound( os.path.join('data','claws.ogg') )

    #--------- create Sprites
    hunter = BirdCatcher()

    # create the first parallax scrolling mountains
    Mountain(1) # blue
    Mountain(2) # pink
    Mountain(3) # red

    mainloop = True
    while mainloop:
        seconds = clock.tick(fps)/1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                mainloop = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    printSpriteList()
                if e.key == pygame.K_g: # toggle gravity
                    pass
                    #printBirds()
                    #Fragment.gravity = not Fragment.gravity
        # pygame.sprite.spritecollide(sprite,group,dokill,collide=None): return Sprite list
        # pygame.sprite.collide_circle works ONLY IF sprite has self.radius
        # -------- clean, draw, update, flip -----------------
        allgroup.clear(screen, bgsurf)
        allgroup.update(seconds)
        allgroup.draw(screen)
        pygame.display.flip()

def printSpriteList():
    print '==========================='
    print '------- Sprite list -------'
    spritelist = allgroup.get_sprites_at(pygame.mouse.get_pos())
    for sprite in spritelist:
        print sprite, 'Layer:',allgroup.get_layer_of_sprite(sprite)
    print '---------------------------'
    print 'top layer:',allgroup.get_top_layer()
    print 'bottome layer:', allgroup.get_bottom_layer()
    print 'layers:',allgroup.layers()
    print '==========================='

if __name__ == '__main__':
    main()
