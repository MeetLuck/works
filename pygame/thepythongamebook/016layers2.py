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

class BirdCatcher(pygame.sprite.Sprite):
    # circle around the mouse pointer. 
    # LEFT button create new sprite, RIGHT button kill sprite
    def __init__(self):
        self._layer = 9
        self.groups = stuffgroup#, allgroup
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (100,100) )
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 50
        pygame.draw.circle(self.image,red,(self.radius,self.radius), self.radius, 2)
    def update(self,seconds):
        self.rect.center = pygame.mouse.get_pos()

class Lifebar(pygame.sprite.Sprite):
    # show a bar with the hitpoints of a Bird sprite with a given bossnumber
    # Lifebar class can identify the boss(Bird sprite) with this codeline: Bird.birds[bossnumber]
    def __init__(self,bossnumber):
        self.bossnumber = bossnumber
        self._layer = Bird.birds[self.bossnumber]._layer
        self.groups = lifebargroup, allgroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        # 
        self.bird = Bird.birds[self.bossnumber]
        self.width = self.bird.rect.width
        self.image = pygame.Surface( (self.width,7) )
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image,green, (0,0,self.width,7), 1)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.oldpercent = 0
    def update(self,time):
        self.percent = self.bird.hitpoints/self.bird.hitpointsfull
        if self.percent != self.oldpercent:
            pygame.draw.rect(self.image,black,(1,1,self.width-2,5))
            pygame.draw.rect(self.image,green,(1,1,int(self.width*self.percent),5),0 )
            #pygame.draw.rect(self.image, (0,0,0), (1,1,Bird.birds[self.bossnumber].rect.width-2,5)) # fill black
            #pygame.draw.rect(self.image, (0,255,0), (1,1,int(Bird.birds[self.bossnumber].rect.width * self.percent),5),0) # fill green
        self.oldpercent = self.percent
        self.rect.centerx = self.bird.rect.centerx
        self.rect.centery = self.bird.rect.centery - self.bird.rect.height/2 - 10
        # check if boss is still alive
        if self.bird.hitpoints < 1.0: 
            self.kill() # using base class method

class Bird(pygame.sprite.Sprite):
    images = []
    birds = {}  # a dictionary of all birds, each bird has its own number
    number = 0
    waittime = 1.0 # seconds
    hitpointsfull = 100.0
    def __init__(self,layer=4):
        self._layer = layer
        self.groups = birdgroup,allgroup
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x,self.y = random.randint(50,screenwidth-50), random.randint(25,screenheight-25)
        self.image = Bird.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = -100,-100 # out of screen, not visible
        self.dx,self.dy = 0,0
        self.radius = max(self.rect.width,self.rect.height)/2.0
        #self.hitpointsfull = 100.0
        self.hitpoints = Bird.hitpointsfull
        #self.lifetime = 0.0
        self.cleanStatus() #self.catched = self.crashing = False
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self 
        Lifebar(self.number) # create a Lifebar for self
        # starting imposion of blue fragments
        #for _ in range(8):
        #   Fragment(self.pos, True)
    def newSpeed(self):
        randomdirection = random.choice([-1,1])
        self.dx = random.randint(BIRDSPEEDMIN,BIRDSPEEDMAX) * randomdirection
        self.dy = random.randint(BIRDSPEEDMIN,BIRDSPEEDMAX) * randomdirection
    def cleanStatus(self):
        self.catched = self.crashing = False
    def kill(self):
        # a shower of red fragements, exploding outwards
        for _ in range(20):
            Fragment(self.pos)
        pygame.sprite.Sprite.kill(self)
    def update(self,seconds):
        self.move(seconds)
        self.checkScreenPosition()
        #--- calculate actual image: crashing, catched, both, nothing
        self.image = Bird.images[self.crashing+2*self.catched ]
        #--- calculate new position on screen
        self.rect.center = self.pos
        #--- loose hitpoints(health)
        if self.crashing: self.hitpoints -= 1
        if self.hitpoints <= 0 : self.kill()
    def move(self,seconds):
        # speed limit
        if abs(self.dx) > BIRDSPEEDMAX: self.dx = BIRDSPEEDMAX
        if abs(self.dy) > BIRDSPEEDMAX: self.dy = BIRDSPEEDMAX
        self.x += self.dx * seconds
        self.y += self.dy * seconds

    def checkScreenPosition(self): # check if Bird out of screen
        screenrect = screen.get_rect()
        width,height = self.rect.width, self.rect.height
        if not screenrect.contains(self.rect): # out of screen
            if self.x + width/2 > screenrect.right:
                self.x = screenrect.right - width/2
            if self.x - width/2 < screenrect.left:
                self.x = screenrect.left + width/2
            if self.y + height/2 > screenrect.bottom:
                self.y = screenrect.bottom - height/2
            if self.y - height/2 < screenrect.top:
                self.y = screenrect.top + height/2
            self.newSpeed() # calculate new direction

    @property
    def pos(self):
        return (self.x,self.y)

class Fragment(pygame.sprite.Sprite):
    gravity = False 

    def __init__(self, pos):
        self.groups = fraggroup, allgroup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._layer = 9
        self.x,self.y = 0,0
        self.target = pos
        self.fragmentmaxspeed = 0.8*BIRDSPEEDMAX
        # red fragment explodes from the bird toward screen edge
        self.color = randomred
        self.x,self.y = pos
        self.dx = random.randint(-self.fragmentmaxspeed, self.fragmentmaxspeed)
        self.dy = random.randint(-self.fragmentmaxspeed, self.fragmentmaxspeed)
        self.image = pygame.Surface( (10,10) )
        self.image.set_colorkey(black)
        fragment_radius = random.choice( [1,1,1,2,2,2,3,3,4] )
        pygame.draw.circle(self.image, self.color, (5,5),fragment_radius)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.lifetime = random.random()
        self.time = 0.0

    def update(self,seconds):
        self.time += seconds
        if self.time > self.lifetime: self.kill()
        self.x += 0.5 * seconds * self.dx
        self.y += 0.5 * seconds * self.dy
        if Fragment.gravity:
            self.dy += FORCEOFGRAVITY
        self.rect.center = self.pos

    @property 
    def pos(self):
        return self.x,self.y


#--- define sprite Group before creating sprites
#blockgroup = pygame.sprite.LayeredUpdates()
birdgroup = pygame.sprite.Group()
textgroup = pygame.sprite.Group()
lifebargroup = pygame.sprite.Group()
fraggroup = pygame.sprite.Group()
#mountaingroup = pygame.sprite.Group()

# only allgroup draws the sprite, so use LayeredUpdates() instead Group()
allgroup = pygame.sprite.LayeredUpdates() # can draw sprites in layers

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

    #--- load images into classes(class attributes)
    Bird.images.append( pygame.image.load(os.path.join('data','babytux.png')) ) # Bird.images[0]
    Bird.images.append( pygame.image.load(os.path.join('data','babytux_neg.png')) ) # Bird.images[1]
    Bird.images.append( Bird.images[0].copy() ) # Bird.images[2]
    Bird.images.append( Bird.images[1].copy() ) # Bird.images[3]
    #--- draw blue border on images 2,3 
    pygame.draw.rect( Bird.images[2],blue,(0,0,32,36),1 )
    pygame.draw.rect( Bird.images[3],blue,(0,0,32,36),1 )
    #--- conver_alpha()
    for i in range(3): # 0,1,2,3
        Bird.images[i] = Bird.images[i].convert_alpha()
    #--- load sound
    crysound = pygame.mixer.Sound( os.path.join('data','claws.ogg') )

    #--------- create Sprites
    #hunter = BirdCatcher()

    birdlayer = 4
    birdtext = Text('current Bird layer = %i' %birdlayer)
    cooldowntime = 0 # seconds

    # start with some Birds
    for _ in range(30):
        Bird(birdlayer) # one single Bird

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
                    printBirds()
                    Fragment.gravity = not Fragment.gravity
        # change bird layer on mouse click
        leftmouse,_,rightmouse = pygame.mouse.get_pressed()
        if leftmouse and birdlayer < 10:
            birdlayer += 1
            crysound.play()
            for bird in birdgroup:
                allgroup.change_layer(bird,birdlayer)
        if rightmouse and birdlayer > -4:
            birdlayer -= 1
            crysound.play()
            for bird in birdgroup:
                allgroup.change_layer(bird,birdlayer)
        pygame.display.set_caption("fps: %.2f birds: %i grav: %s" % (clock.get_fps(), len(birdgroup),
                                    Fragment.gravity))
        birdtext.newMsg('current Bird layer = %i' %birdlayer) # update text for birdlayer
        # --------------- collision detection ----------------
        for bird in birdgroup:
            bird.cleanStatus()
        # pygame.sprite.spritecollide(sprite,group,dokill,collide=None): return Sprite list
        #crashgroup = pygame.sprite.spritecollide(hunter,birdgroup,False,pygame.sprite.collide_circle)
        # pygame.sprite.collide_circle works ONLY IF sprite has self.radius
        #for crashbird in crashgroup:
        #   crashbird.catched = True # will get a blue border from Bird.update()
        for bird in birdgroup:  # test if a bird collide with another bird
            # check Bird.number to make sure the bird is NOT crashing with himself
            crashgroup = pygame.sprite.spritecollide(bird,birdgroup,False)
            for crashbird in crashgroup:
                if crashbird.number != bird.number: # different number means different birds
                    bird.crashing = True
                    bird.dx -= crashbird.x - bird.x
                    bird.dy -= crashbird.y - bird.y
        # create 10 new Birds if fewer than 11 birds alive
        if len(birdgroup) < 10:
            for _ in range(random.randint(1,5)):
                Bird(birdlayer)
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

def printBirds():
    print len(Bird.birds)
    for bird in Bird.birds:
        print Bird.birds[bird]
if __name__ == '__main__':
    main()
