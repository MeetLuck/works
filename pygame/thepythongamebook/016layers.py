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

class Block(pygame.sprite.Sprite):
    # a block with a number indicating it's layer
    # Blocks move horizontal and bounce on screen edges
    def __init__(self, blockNum=1):
        self.groups = blockgroup, allgroup
        self.blockNum = blockNum
        self._layer = self.blockNum
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.screenrect = screen.get_rect()
        self.image = pygame.Surface( (100,100))
        self.color = random.randint(10,255), random.randint(10,255), random.randint(10,255)
        self.image.fill(self.color)
        self.image.blit( write(str(self.blockNum)), (40,40) )
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = 50 + 100*self.blockNum
        self.rect.centery = screen.get_height()/2
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.dx, self.dy = 0,random.randint(50,100) * random.choice([-1,1])

    def newDirection(self):
        self.dy *= -1 # toggle y direction

    def update(self,time):
        if not self.screenrect.contains(self.rect): # Out Of screen
            # compare self.rect and screen.rect
            if self.y < self.screenrect.top:
                self.y = self.screenrect.top
            elif self.y > self.screenrect.bottom:
                self.y = self.screenrect.bottom
                self.newDirection() # opposite y direction
        self.x += self.dx * time
        self.y += self.dy * time
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

class BirdCatcher(pygame.sprite.Sprite):
    # circle around the mouse pointer. 
    # LEFT button create new sprite, RIGHT button kill sprite
    def __init__(self):
        self._layer = 9
        self.groups = stuffgroup, allgroup
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
        self.groups = bargroup, allgroup
        self.bossnumber = bossnumber
        self._layer = Bird.birds[self.bossnumber]._layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.bird = Bird.birds[self.bossnumber]
        self.width = self.bird.rect.width
        self.image = pygame.Surface( (self.width,7) )
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image,green, (0,0,self.width,7), 1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0
    def update(self,time):
        self.percent = self.bird.hitpoints/self.bird.hitpointsfull
        if self.percent != self.oldpercent:
            pygame.draw.rect(self.image,black,(1,1,self.width-2,5))
            pygame.draw.rect(self.image,green,(1,1,self.width*self.percent,5),0)
        self.oldpercent = self.percent
        self.rect.centerx = self.bird.rect.centerx
        self.rect.centery = self.bird.rect.centery - self.bird.rect.height/2 - 10
        # check if boss is still alive
        if self.bird.hitpoints < 1: 
            self.kill() # using base class method

class Bird(pygame.sprite.Sprite):
    images = []
    birds = {}  # a dictionary of all birds, each bird has its own number
    number = 0
    waittime = 1.0 # seconds
    def __init__(self,layer=4):
        self.groups = birdgroup,allgroup
        self._layer = layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x,self.y = random.randint(50,screenwidth-50), random.randint(25,screenheight-25)
        self.screenrect = screen.get_rect()
        self.image = Bird.images[0]
        self.hitpointsfull = 100
        self.hitpoints = 100
        self.rect = self.image.get_rect()
        self.radius = max(self.rect.width,self.rect.height)/2.0
        self.dx,self.dy = 0,0
        self.lifetime = 0.0
        self.waittime = Bird.waittime
        self.waiting = True
        self.rect.center = -100,-100 # out of screen, not visible
        self.cleanStatus()
        self.catched = self.crashing = False
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self 
        Lifebar(self.number) # create a Lifebar for self
        # starting imposion of blue fragments
        for _ in range(8):
            Fragment(self.pos, True)
    def newSpeed(self):
        randomdirection = random.choice([-1,1])
        self.dx = random.randint(BIRDSPEEDMIN,BIRDSPEEDMAX) * randomdirection
        self.dy = random.randint(BIRDSPEEDMIN,BIRDSPEEDMAX) * randomdirection
    def cleanStatus(self):
        self.catched = False
        self.crashing = False
    def kill(self):
        # a shower of red fragements, exploding outwards
        for _ in range(15):
            Fragment(self.pos)
        pygame.sprite.Sprite.kill(self)
    def update(self,seconds):
        # --- make Bird only visible after waiting time
        self.lifetime += seconds
        if self.lifetime > self.waittime and self.waiting:
            self.newSpeed()
            self.waiting = False
            self.rect.center = self.pos
        if self.waiting:
            self.rect.center = -100,-100
        else:
            # friction = 0.99, make it slower
            if abs(self.dx) > BIRDSPEEDMIN and abs(self.dy) > BIRDSPEEDMIN:
                self.dx *= FRICTION
                self.dy *= FRICTION
            # speed limit
            if abs(self.dx) > BIRDSPEEDMAX:
                self.dx = BIRDSPEEDMAX
            if abs(self.dy) > BIRDSPEEDMAX:
                self.dy = BIRDSPEEDMAX
            # move bird
            self.x += self.dx * seconds
            self.y += self.dy * seconds
            #self.pos = x,y
            # check if Bird out of screen
            if not self.screenrect.contains(self.rect): # out of screen
                width,height = self.rect.width,self.rect.height
                if self.x + width/2 > self.screenrect.right:
                    self.x = self.screenrect.right - width/2
                if self.x - width/2 < self.screenrect.left:
                    self.x = self.screenrect.left + width/2
                if self.y + height/2 > self.screenrect.bottom:
                    self.y = self.screenrect.bottom - height/2
                if self.y - height/2 < self.screenrect.top:
                    self.y = self.screenrect.top + height/2
                self.newSpeed() # calculate new direction
            #--- calculate actual image: crashing, catched, both, nothing
            self.image = Bird.images[self.crashing + 2*self.catched]
            #--- calculate new position on screen
            self.rect.center = self.pos
            #--- loose hitpoints(health)
            if self.crashing: self.hitpoints -= 1
            if self.hitpoints <= 0 : self.kill()
    @property
    def pos(self):
        return (self.x,self.y)

class Fragment(pygame.sprite.Sprite):
    gravity = False 
    def __init__(self, pos,bluefrag=False):
        self._layer = 9
        self.groups = stuffgroup, allgroup
        self.bluefrag = bluefrag
        self.x,self.y = 0,0
        self.target = self.pos
        self.fragmentmaxspeed = 2*BIRDSPEEDMAX
        if self.bluefrag:
            # blue fragment implodes from screen edge toward Bird
            self.color = randomblue
            self.side = random.randint(1,4)
            if self.side == 1:
                self.x = 0 # left side
                self.y = random.randint(0,screenheight)
            elif self.side == 2:
                self.x = random.randint(0,screenwidth)
                self.y = 0 # top side
            elif self.side == 3:
                self.x = screenwidth    # right side
                self.y = random.randint(0,screenheight)
            elif self.side == 4:
                self.x = random.randint(0,screenwidth)
                self.y = screenheight    # right side
            # calculate fly time for one seconds... 
            self.dx = self.target[0] - self.x
            self.dy = self.target[1] - self.y
            self.lifetime = Bird.waittime + random.random()/2.0
        else:
            # red fragment explodes from the bird toward screen edge
            self.color = randomred
            self.x,self.y = pos
            self.dx = random.randint(-self.fragmentmaxspeed, self.fragementmaxspeed)
            self.dy = random.randint(-self.fragmentmaxspeed, self.fragementmaxspeed)
            self.lifetime = 1 + 3*random.random()
        self.image = pygame.Surface( (10,10) )
        self.image.set_colorkey(black)
        pygame.draw.circle(self.image, self.color, (5,5), random.randint(2,5) )
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.time = 0.0

    def update(self,seconds):
        self.time += seconds
        if self.time > self.lifetime: self.kill()
        self.x += seconds * self.dx
        self.y += seconds * self.dy
        if Fragment.gravity and not self.bluefrag:
            self.dy += FORCEOFGRAVITY
        self.rect.center = self.pos

    @property 
    def pos(self):
        return self.x,self.y


def main():
    global stuffgroup,bargroup,textgroup,birdgroup,blockgroup,allgroup,mountaingroup
    # draw background
    bgsurf = pygame.Surface( screensize )
    bgsurf.fill(white)
    bgsurf.blit(write("press left mouse button to increase Bird's layer"),(50,40))
    bgsurf.blit(write("press right mouse button to decrease Bird's layer."),(50,65))
    bgsurf.blit(write("layer of mountains are: -1 (blue), -2 (pink), -3 (red)"),(50,90))
    bgsurf.blit(write("Press ESC to quit, p to print info at mousepos"), (50,115))
    bgsurf = bgsurf.convert_alpha()
    screen.blit(bgsurf,(0,0) )

    #--- define sprite Group before creating sprites
    blockgroup = pygame.sprite.LayeredUpdates()
    birdgroup = pygame.sprite.Group()
    textgroup = pygame.sprite.Group()
    bargroup = pygame.sprite.Group()
    stuffgroup = pygame.sprite.Group()
    mountaingroup = pygame.sprite.Group()

    # only allgroup draws the sprite, so use LayeredUpdates() instead Group()
    allgroup = pygame.sprite.LayeredUpdates() # can draw sprites in layers
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
    hunter = BirdCatcher()

#   for i in range(screenwidth/100):
#       Block(i)

    othergroup = [] # for collision detection
    badcoding = False

    birdlayer = 4
    birdtext = Text('current Bird layer = %i' %birdlayer)
    cooldowntime = 0 # seconds

    # start with some Birds
    for _ in range(5):
        Bird(birdlayer) # one single Bird

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
                if e.key == pygame.K_g: # toggle gravity
                    Fragment.gravity = not Fragment.gravity

            # change bird layer on mouse click
            leftmouse,_,rightmouse = pygame.mouse.get_pressed()
            if cooldowntime <= 0:
                if leftmouse and birdlayer < 10:
                    birdlayer += 1
                    cooldowntime = 0.5 # seconds
                    crysound.play()
                    for bird in birdgroup:
                        allgroup.change_layer(bird,birdlayer)
                    for bar in bargroup:
                        allgroup.change_layer(bar,birdlayer)
                if rightmouse and birdlayer > -4:
                        birdlayer -= 1
                        cooldowntime = 0.5
                        crysound.play()
                        for bird in birdgroup:
                            allgroup.change_layer(bird,birdlayer)
                        for bar in bargroup:
                            allgroup.change_layer(bar,birdlayer)
            else:
                cooldowntime -= seconds   # avoid speed clicking
            pygame.display.set_caption("fps: %.2f birds: %i grav: %s" % (clock.get_fps(), len(birdgroup),
                                        Fragment.gravity))
            birdtext.newMsg('current Bird layer = %i' %birdlayer) # update text for birdlayer
            # --------------- collision detection ----------------
            for bird in birdgroup:
                bird.cleanStatus()
            # pygame.sprite.spritecollide(sprite,group,dokill,collide=None): return Sprite list
            crashgroup = pygame.sprite.spritecollide(hunter,birdgroup,False,pygame.sprite.collide_circle)
            # pygame.sprite.collide_circle works ONLY IF sprite has self.radius
            for crashbird in crashgroup:
                crashbird.catched = True # will get a blue border from Bird.update()
            for bird in birdgroup:  # test if a bird collide with another bird
                # check Bird.number to make sure the bird is NOT crashing with himself
                crashgroup = pygame.sprite.spritecollide(bird,birdgroup,False)
                for crashbird in crashgroup:
                    if crashbird.number != bird.number: # different number means different birds
                        bird.crashing = True
                        if not bird.waiting:
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

if __name__ == '__main__':
    main()
