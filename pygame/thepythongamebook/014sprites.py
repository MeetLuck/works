"""
014sprites.py
create more sprites with mouse click.
show collision detection
"""
from constants import *

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
screen = pygame.display.set_mode( (640,480) )
BIRDSPEED = 50

def write(msg):
    sysfont = pygame.font.SysFont('None', 32)
    textsurf = sysfont.render(msg,True,black)
    textsurf = textsurf.convert_alpha()
    return textsurf

class BirdCatcher(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface( (100,100) )
        self.image.set_colorkey(black)
        pygame.draw.circle(self.image, red, (50,50),50,2)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = 50 # for collide check
    def update(self,seconds):
        self.rect.center = pygame.mouse.get_pos()

class Bird(pygame.sprite.Sprite):
    images = [] # list of all images
    birds = {}  # dict of all birds, each bird has its own number
    number = 0
    def __init__(self, startpos=(50,50), screenrect = screen.get_rect()):
        #pygame.sprite.Sprite.__init__(self, *groups)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = startpos
        self.x,self.y = self.pos
        self.image = Bird.images[0]
        self.rect = self.image.get_rect()
        self.screenrect = screenrect # screen rect
        self.newSpeed()
        self.catched = False
        # not necessary
        self.number = Bird.number # get my personal Birdnumber
        Bird.number += 1
        Bird.birds[self.number] = self # store self into the Bird dictionary
    def newSpeed(self):
        randomspeed = random.choice( [-1,+1] )
        self.dx = randomspeed + random.random() * BIRDSPEED * randomspeed
        self.dy = randomspeed + random.random() * BIRDSPEED * randomspeed
    def update(self,seconds):
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        # check if it's out of screen
        if not self.screenrect.contains(self.rect):
            self.image = Bird.images[1] # crash into wall
            # compare self.rect and screen.rect
            if self.x + self.rect.width/2 > self.screenrect.right:
                self.x = self.screenrect.right - self.rect.width/2
            if self.x - self.rect.width/2 < self.screenrect.left:
                self.x = self.screenrect.left + self.rect.width/2
            if self.y + self.rect.height/2 > self.screenrect.bottom:
                self.y = self.screenrect.bottom - self.rect.height/2
            if self.y - self.rect.height/2 < self.screenrect.top:
                self.y = self.screenrect.top + self.rect.height/2
            self.newSpeed() # calculate a new direction
        else:
            if self.catched:
                self.image = Bird.images[2] # blue rectangle
            else:
                self.image = Bird.images[0] # normal bird image
        # calculate new position on screen
        self.rect.centerx = round(self.x,0)
        self.rect.centery = round(self.y,0)

bgsurf = pygame.Surface( screen.get_size() )
bgsurf.fill(white)
bgsurf.blit(write("Press left mouse button for more sprites. Press ESC to quit"),(5,10))
bgsurf = bgsurf.convert()
screen.blit(bgsurf,(0,0))
clock = pygame.time.Clock()
fps = 60
# load images into class( class attributes )
Bird.images.append(pygame.image.load(os.path.join('data','babytux.png')))
Bird.images.append(pygame.image.load(os.path.join('data','babytux_neg.png')))
Bird.images.append(Bird.images[0].copy())
pygame.draw.rect(Bird.images[2],blue,(0,0,32,36),2) # blue border
for i in range(3):
    Bird.images[i] = Bird.images[i].convert_alpha()

# define Bird.groups to pass them to pygame.sprite.Sprite.__init__(self,*groups)
birdgroup = pygame.sprite.Group()
allgroup  = pygame.sprite.Group()
Bird.groups = birdgroup, allgroup
BirdCatcher.groups = allgroup
# one single Bird
Bird()
hunter = BirdCatcher()

mainloop = True
while mainloop:
    miliseconds = clock.tick(fps)
    period = miliseconds/1000.0
    mainloop = checkForQuit()
    # create new Bird on mouseclick
    if pygame.mouse.get_pressed()[0]:
        Bird(pygame.mouse.get_pos()) # create a new Bird at mousepos
    pygame.display.set_caption("[FPS]: %.2f birds: %i" % (clock.get_fps(), len(birdgroup)))
    # collision detection
    for bird in birdgroup:
        bird.catched = False # set all Bird sprites to not catched
    # pygame.sprite.spritecollide(sprite, group,dokill, collide=None): return Sprite list
    crashgroup = pygame.sprite.spritecollide(hunter, birdgroup, False, pygame.sprite.collide_circle)
    # pygame.sprite.collide_circle works only if one sprite has self.radius
    # you can do without that argument collided and only the self.rects will be checked
    for crashbird in crashgroup:
        crashbird.catched = True  # will get a blue border from Bird.update()
        #crashbird.kill() # this would remove him from all his groups

    allgroup.clear(screen, bgsurf)
    allgroup.update(period)
    allgroup.draw(screen)
    pygame.display.flip()

