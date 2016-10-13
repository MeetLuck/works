# 015 more sprites.py
# pygame sprites with hit bars and exploding fragments
# pygame sprites moving around and exploding into little fragements
# effect of gravity on the fragements can be toggled
# different coding style and its outcome on performance(frame rate)
# can be toggled and is displayed by green bars. 
# a long bar indicates a slow performance
from constants015 import *

# define sprite groups
birdgroup = pygame.sprite.LayeredUpdates()
bargroup = pygame.sprite.Group()
stuffgroup = pygame.sprite.Group()
fragmentgroup = pygame.sprite.Group()
# LayedUpdates intead of group to draw in correct order
allgroup = pygame.sprite.LayeredUpdates() # more sophisticated than simple group

class BirdCatcher(pygame.sprite.Sprite):
    # circle around the mouse pointer. Left button create new sprite, right button kill sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.image = pygame.Surface( (100,100) )
        self.image.set_colorkey(black) # make black transparent
        pygame.draw.circle(self.image,red,(50,50),50,2) # red circle
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = 50
    def update(self,seconds):
        # no need for seconds, but other sprites need it
        self.rect.center = pygame.mouse.get_pos()
class Fragment(pygame.sprite.Sprite):
    # a fragment of an exploding Bird
    gravity = True # fragments fall down
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = 0.0, 0.0
        self.x, self.y = self.pos
        self.image = pygame.Surface( (10,10) )
        self.image.set_colorkey(black)
        color = random.randint(1,64), 0, 0
        pygame.draw.circle(self.image,color,(5,5),random.randint(2,5) )
        self.image = self.image.conver_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
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
        self.boss = boss
        self.image = pygame.Surface( (self.boss.rect.width, 7) )
        self.image.set_colorkey(black)
        pygame.draw.rect( self.image, green, (0,0,self.boss.rect.width,7), 1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0
        self.bossnumber = self.boss.number # the unique number (name) of my boss
    def update(self,time):
        self.percent = self.boss.hitpoints/self.boss.hitpointsfull * 1.0
        if self.percent != self.oldprecent:
            pygame.draw.rect(self.image,black,(1,1,self.boss.rect.width-2.5)) 
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
    images = []  # list of all images
    birds = []   # dict of all Birds, each Bird has its own number
    number = 0   # Bird number
    def __init__(self,startpos=screen.get_rect().center):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = 0.0,0.0
        self.x,self.y = self.pos
        self.screenrect = screen.get_rect()
        self.image = Bird.image[0]
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
        LiveBar(self) # create a Livebar for this Bird
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
    def cleanStatus(self):
        self.catched = False # set all Bird sprites to not catched
        self.crashing = False
    def update(self, seconds):
        # friction makes birds slower
        if abs(self.dx) > BIRDSPEEDMIN and abs(self.dy) > BIRDSPEEDMIN:
            self.dx *= FRICTION
            self.dy *= FRICTION
        # speed limit
        if abs(self.dx) > birdspeedmax:
            self.dx = BIRDSPEEDMAX 
        if abs(self.dy) > birdspeedmax:
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
        self.image = Bird.image[self.crashing + 2*self.catched]
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
    img = img.convert_alpha() # Bird.images[i] = Bird.images[i].conver_alpha()
cry = pygame.mixer.sound( os.path.join('data','claws.ogg')) # load sound

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

mainloop = 60
while mainloop:
    miliseconds = clock.tick(fps) # miliseconds passed last frame

