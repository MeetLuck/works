# 015 more sprites.py
# pygame sprites with hit bars and exploding fragments
# pygame sprites moving around and exploding into little fragements
# effect of gravity on the fragements can be toggled
# different coding style and its outcome on performance(frame rate)
# can be toggled and is displayed by green bars. 
# a long bar indicates a slow performance
from constants015 import *


class BirdCatcher(pygame.sprite.Sprite):
    # circle around the mouse pointer. Left button create new sprite, right button kill sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (100,100) )
        self.image.set_colorkey(black) # make black transparent
        self.radius = 50
        pygame.draw.circle(self.image,red,(50,50),self.radius,2) # red circle
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
    def update(self,seconds):
        # no need for seconds, but other sprites need it
        self.rect.center = pygame.mouse.get_pos()
'''
class Fragment(pygame.sprite.Sprite): # a fragment of an exploding Bird
    gravity = True # fragments fall down
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self,self.groups)
        #self.pos = pos #[0.0, 0.0]
        self.x, self.y = pos
        self.image = pygame.Surface( (10,10) )
        self.image.set_colorkey(black)
        # draw circle with random color and random radius
        randcolor = random.randint(10,64), 0, 0  # dark red
        randradius = random.randint(2,5)
        pygame.draw.circle(self.image, randcolor, (5,5), randradius)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos 
        self.lifetime = 1 + 5*random.random()
        self.time = 0.0
        self.fragmentmaxspeed = 2*BIRDSPEEDMAX
        self.dx = random.randint( -self.fragmentmaxspeed, self.fragmentmaxspeed)
        self.dy = random.randint( -self.fragmentmaxspeed, self.fragmentmaxspeed)
    def update(self,seconds):
        self.time += seconds
        if self.time > self.lifetime: self.kill()
        self.x += seconds * self.dx
        self.y += seconds * self.dy
        if Fragment.gravity:
            self.dy += FORCEOFGRAVITY # gravity suck fragments down
        self.rect.centerx = round(self.x,0)
        self.rect.centery = round(self.y,0)
'''
class Fragment(pygame.sprite.Sprite):
    """a fragment of an exploding Bird"""
    gravity = True # fragments fall down ?
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0.0,0.0]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.image = pygame.Surface((10,10))
        self.image.set_colorkey((0,0,0)) # black transparent
        pygame.draw.circle(self.image, (random.randint(1,64),0,0), (5,5), 
                                        random.randint(2,5))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
        self.lifetime = 1 + random.random()*5 # max 6 seconds
        self.time = 0.0
        self.fragmentmaxspeed = BIRDSPEEDMAX * 2 # try out other factors !
        self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        
    def update(self, seconds):
        self.time += seconds
        if self.time > self.lifetime:
            self.kill() 
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        if Fragment.gravity:
            self.dy += FORCEOFGRAVITY # gravity suck fragments down
        self.rect.centerx = round(self.pos[0],0)
        self.rect.centery = round(self.pos[1],0)

class Timebar(pygame.sprite.Sprite):
    # shows a bar as long as how much miliseconds are passed between two frames
    def __init__(self,long):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.long = 2 * long
        self.image = pygame.Surface( (self.long,5) )
        self.image.fill( (128,255,0) )  # green with red
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = 0, screen.get_height()
    def update(self,time):
        self.rect.centery -= 7 
        if self.rect.centery < 0: self.kill()

class Livebar(pygame.sprite.Sprite):
    # show a bar with hitpoints of a Bird sprite
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.boss = boss # bird, Livebar object is a member of Bird object 
        self.width  = self.boss.rect.width
        self.height = 7
        self.image = pygame.Surface( (self.width, self.height) )
        self.image.set_colorkey(black)
        # draw live-bar OVER boss-image
        livebar_rect = 0,0,self.width,self.height
        pygame.draw.rect( self.image, green, livebar_rect, 1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0
        self.bossnumber = self.boss.number # the unique number (name) of my boss
    def update(self,time):
        self.percent = self.boss.hitpoints/self.boss.hitpointsfull
        if self.percent != self.oldpercent:
            pygame.draw.rect(self.image,black,(1,1,self.boss.rect.width-2,5)) 
            greenrect = 1,1, int(self.boss.rect.width*self.percent),5
            pygame.draw.rect(self.image,green,greenrect,0)
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = self.boss.rect.centery - self.boss.rect.height/2 - 10
        # check if boss is still alive
        if not Bird.birds[self.bossnumber]:
            self.kill() # kill the hitbar

class Bird(pygame.sprite.Sprite):
    # a nice little sprite that bounce off walls and other sprites
    images = list()   # list of all images
    birds  = dict()   # dict of all Birds, each Bird has its own number
    number = 0        # Bird number
    def __init__(self,startpos=screen.get_rect().center):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x,self.y = startpos 
        #self.pos = self.x, self.y
        self.screenrect = screen.get_rect()
        self.image = Bird.images[0]
        self.hitpointsfull = float(HITPOINTS)  # maximal hitpoints
        self.hitpoints = float(HITPOINTS)
        self.rect = self.image.get_rect()
        self.radius = max(self.rect.width, self.rect.height)/2.0

        self.setNewSpeed()
        self.cleanStatus()
        self.catched = False
        self.crashing = False
        # --- not necessary
        self.number = Bird.number # get my personal Bird number
        Bird.number += 1
        Bird.birds[self.number] = self # store self into Bird dict
        #print "my number %i Bird number %i " % (self.number, Bird.number)
        Livebar(self) # create a Livebar for this Bird
    def setNewSpeed(self):
        # new birdspeed, but not 0
        randomspeed = random.choice([-1,1])
        self.dx = randomspeed + randomspeed * random.random() * BIRDSPEEDMAX
        self.dy = randomspeed + randomspeed * random.random() * BIRDSPEEDMAX
    def kill(self):
        # because i want to do some special effects(sound, dict etc)
        # before killing the Bird sprite i have to write my own kill(self)
        # and finally call pygame.sprite.Sprite.kill(self)
        # to do 'real' killing
        cry.play()
        for _ in range( random.randint(3,15) ):
            Fragment(self.pos)
        Bird.birds[self.number] = None # kill Bird in sprite dict
        pygame.sprite.Sprite.kill(self)
    @property
    def pos(self): # AUTOMATICALLY CHANGE self.pos if self.x,self.y changes
        return self.x,self.y
    # instead of using property, we can use list
    # self.pos = [0,0]
    # self.pos[0],self.pos[1] = startpos

    def cleanStatus(self):
        self.catched = False # set all Bird sprites to not catched
        self.crashing = False
    def update(self, seconds):
        # friction makes birds slower
        if abs(self.dx) > BIRDSPEEDMIN and abs(self.dy) > BIRDSPEEDMIN:
            self.dx *= FRICTION   # 0.99 -> 1% slower every update !!!
            self.dy *= FRICTION   # 0.99 -> 1% slower every update !!!
        # speed limit
        if abs(self.dx) > BIRDSPEEDMAX:
            self.dx = BIRDSPEEDMAX 
        if abs(self.dy) > BIRDSPEEDMAX:
            self.dy = BIRDSPEEDMAX
        # new position
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        # check if Bird out of screen
        if not self.screenrect.contains(self.rect):
            self.crashing = True # change  color later
            # compare self.rect and screen.rect
            # check right side
            if self.x + self.rect.width/2 > self.screenrect.right:
                self.x = self.screenrect.right - self.rect.width/2
            # check left side
            if self.x - self.rect.width/2 < self.screenrect.left:
                self.x = self.screenrect.left + self.rect.width/2
            # check bottom side
            if self.y + self.rect.height/2 > self.screenrect.bottom:
                self.y = self.screenrect.bottom - self.rect.height/2
            # check top side
            if self.y - self.rect.height/2 < self.screenrect.top:
                self.y = self.screenrect.top + self.rect.height/2
            self.setNewSpeed() # calculate a new direction

        #---- calculate actual image : crashing, catched, both, or nothing
        # Bird.images[0] -> babytux
        # Bird.images[1] -> babytux_neg
        # Bird.images[2] -> babytux with blue border,     copy of Bird.images[0]
        # Bird.images[3] -> babytux_neg with blue border, copy of Bird.images[1]
        # crash , catched
        #   0       0     -> Bird.images[0]
        #   1       0     -> Bird.images[1]
        #   0       1     -> Bird.images[2]
        #   1       1     -> Bird.images[3]

        self.image = Bird.images[self.crashing + 2*self.catched]
        #---- calculate new position on screen
        self.rect.centerx = round(self.x,0)
        self.rect.centery = round(self.y,0)
        #---- loose hitpoints
        if self.crashing: self.hitpoints -= 1
        #---- check if still alive
        if self.hitpoints <= 0: self.kill()

# ----------------- no class -------------------------------------------------
bgsurf = pygame.Surface( screen.get_size() )
bgsurf.fill(white)
bgsurf.blit(write("press left mouse button for more sprites."),(150,10))
bgsurf.blit(write("press right mouse button to kill sprites."),(150,40))
bgsurf.blit(write("press g to toggle gravity"),(150,70))
bgsurf.blit(write("press b to toggle bad coding"),(150,100))
bgsurf.blit(write("press c to toggle clever coding"), (150,130))
bgsurf.blit(write("Press ESC to quit"), (150,160))

# paint vertical lines to measure passed time( Timebar )
# for x in range(0, screen.get_width()+1, 20)
for x in range(0,140,20):
    pygame.draw.line(bgsurf,red, (x,0), (x,screen.get_height()), 1)
bgsurf = bgsurf.convert() # jpg can not have transparency
screen.blit(bgsurf, (0,0) )
#pygame.time.wait(2000)

######## Layers ##########
'''
By default, pygame will blit the sprites in the order the sprites are added.
If you prefer PRECISE ORDER of drawing the sprites like mouse pointer always before all other sprites,
you can do TWO THINGs:
* use several clear, update and draw commands, one for each sprite group
* use pygame.sprite.LayeredUpdates group instead of a sprite group and
  set a default layer for each group like in the code below
'''
# define sprite groups
birdgroup = pygame.sprite.LayeredUpdates()
bargroup = pygame.sprite.Group()
stuffgroup = pygame.sprite.Group()
fragmentgroup = pygame.sprite.Group()

# LayedUpdates intead of group to draw IN CORRECT ORDER
allgroup = pygame.sprite.LayeredUpdates() # more sophisticated than simple group

# assing default groups to each sprite class ( only allgroup is useful at the moment )
Livebar.groups      = bargroup, allgroup
Timebar.groups      = bargroup, allgroup
Bird.groups         = birdgroup,allgroup
Fragment.groups     = fragmentgroup, allgroup
BirdCatcher.groups  = stuffgroup, allgroup

# assing default layer for each sprite ( lower number is background )
BirdCatcher._layer = 5 # top foreground
Fragment._layer    = 4
Timebar._layer     = 3
Bird._layer        = 2 
Livebar._layer     = 1

# load images into classes ( class attributes )
Bird.images.append(pygame.image.load(os.path.join('data','babytux.png')))
Bird.images.append(pygame.image.load(os.path.join('data','babytux_neg.png')))
Bird.images.append(Bird.images[0].copy()) # copy of first image = Bird.images[2]
pygame.draw.rect(Bird.images[2],blue,(0,0,32,36),1) # blue border
Bird.images.append(Bird.images[1].copy()) # copy of second image = Bird.images[3]
pygame.draw.rect(Bird.images[3],blue,(0,0,32,36),1) # blue border

for img in Bird.images:
    img = img.convert_alpha() # Bird.images[i] = Bird.images[i].convert_alpha()
cry = pygame.mixer.Sound( os.path.join('data','claws.ogg')) # load sound

# at game start create a Bird and one BirdCatcher
Bird()
hunter = BirdCatcher() # display the BirdCatcher and name it 'hunter'
# set
milimax = 0
othergroup = [] # important for good collision detection
badcoding = False
clevercoding = False
clock = pygame.time.Clock()
fps = 60

mainloop = True
while mainloop:
    miliseconds = clock.tick(fps) # miliseconds passed last frame
    Timebar(miliseconds)
    if miliseconds > milimax: milimax = miliseconds
    seconds = miliseconds/1000.0 # seconds passed since last frame
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            mainloop = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            mainloop = False
        if e.type != pygame.KEYDOWN: continue
        if e.key == pygame.K_g:
            Fragment.gravity = not Fragment.gravity # toggle gravity
        elif e.key == pygame.K_b:
            if badcoding: othergroup = []
            badcoding = not badcoding
            if badcoding: clevercoding = False
        elif e.key == pygame.K_c:
            clevercoding = not clevercoding
            if clevercoding: badcoding = False
        elif e.key == pygame.K_p:
            print '----------'
            print 'toplayer: ', allgroup.get_top_layer()
            print 'bottomlayer: ', allgroup.get_bottom_layer()
            print 'layers: ', allgroup.layers()
    # create a new Bird on mouse click
    if pygame.mouse.get_pressed()[0]:
        Bird(pygame.mouse.get_pos())
    if pygame.mouse.get_pressed()[2]:
        crashgroup = pygame.sprite.spritecollide(hunter, birdgroup, True, pygame.sprite.collide_circle)
    pygame.display.set_caption("ms: %i max(ms): %i fps: %.2f birds: %i gravity: %s bad:%s clever:%s" \
            % (miliseconds, milimax, clock.get_fps(), len(birdgroup), Fragment.gravity, badcoding,\
               clevercoding))
    # collision detection
    for bird in birdgroup:
        bird.cleanStatus()
    # pygame.sprite.spritecollide(sprite, group, dokill, collided = None): return Sprite_list
    crashgroup = pygame.sprite.spritecollide(hunter,birdgroup, False, pygame.sprite.collide_circle)
    # pygame.sprite.collide_circle works ONLY if one sprite has self.radius
    # you can do without that argument collided and ONLY self.rect will be checked
    for crashbird in crashgroup:
        crashbird.catched = True  # will get a blue border from Bird.update()
        # crashbird.kill()  # this would remove him from all his groups
    # test if a bird collides with another bird
    for bird in birdgroup:
        if not clevercoding:
            if badcoding:
                othergroup = birdgroup.copy() # WRONG! this code make ugly time-consuming garbage collection
            else:
                othergroup[:] = birdgroup.sprites() # CORRECT. no garbage collection
            othergroup.remove(bird)  # remove the actual bird, only all other birds remain
            if pygame.sprite.spritecollideany(bird, othergroup):
                crashgroup = pygame.sprite.spritecollide(bird, othergroup,False)
                for crashbird in crashgroup:
                    bird.crashing = True
                    bird.dx -= crashbird.x - bird.x
                    bird.dy -= crashbird.y - bird.y
        else: # very clever coding
            crashgroup = pygame.sprite.spritecollide(bird,birdgroup,False)
            for crashbird in crashgroup:
                if crashbird.number != bird.number: # avoid collision with itself
                    bird.crashing = True  # make a bird blue
                    bird.dx -= crashbird.x - bird.x   # move bird away from other bird
                    bird.dy -= crashbird.y - bird.y
    # ----- clear, draw, update, flip --------------------
    allgroup.clear(screen, bgsurf)
    allgroup.update(seconds)
    allgroup.draw(screen)
    pygame.display.flip()






