import pygame,random,os
from math import pi,sin,cos,atan2
from colors import *
from vector import Vector
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
screensize = screenwidth,screenheight = 640,480
screen = pygame.display.set_mode( screensize )
screenrect = screen.get_rect()
clock = pygame.time.Clock()
fps = 6
#fps = 60
folder = 'data'

def write(msg='pygame is cool',color=black):
    font = pygame.font.SysFont('None',32)
    textsurf = font.render(msg,True,color)
    textsurf = textsurf.convert_alpha()
    return textsurf
def getClassName(classinstance):
    # this function extract the class name of a instance of the class
    text = str(classinstance.__class__) # like <class '__main__.XWing'>
    parts = text.split('.') # [ <class '__main__, XWing'> ]
    return parts[-1][0:-2]  # take all except the last 2 charactors('>)

# ----------------- background artwork -------------  
background = pygame.Surface((screen.get_width(), screen.get_height()))
background.fill((255,255,255))     # fill white
background.blit(write("navigate with w,a,s,d and q and e "),(50,40))
background.blit(write("press SPACE to fire bullets"),(50,70))
background.blit(write("press g to toggle gravity"), (50, 100))
background.blit(write("Press ESC to quit "), (50,130))
background = background.convert()  # jpg can not have transparency
screen.blit(background, (0,0))     # blit background on screen (overwriting all)

# ---------- load sound -----------
crysound = pygame.mixer.Sound(os.path.join(folder,'claws.ogg'))  #load sound
warpsound = pygame.mixer.Sound(os.path.join(folder,'wormhole.ogg'))
bombsound = pygame.mixer.Sound(os.path.join(folder,'bomb.ogg'))
lasersound = pygame.mixer.Sound(os.path.join(folder,'shoot.ogg'))
hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))

#-----------------define sprite groups------------------------
birdgroup = pygame.sprite.Group() 
bulletgroup = pygame.sprite.Group()
fragmentgroup = pygame.sprite.Group()
gravitygroup = pygame.sprite.Group()
# only the allgroup draws the sprite, so i use LayeredUpdates() instead Group()
allgroup = pygame.sprite.LayeredUpdates() # more sophisticated, can draw sprites in layers 

# game constants
BIRDSPEEDMAX = 200
FRAGMENTMAXSPEED = 200
FRICTION = 0.999
FORCEOFGRAVITY = 2.81 # in pixel per seconds
GRAD = 2*pi/360

class Text(pygame.sprite.Sprite):
    def __init__(self,msg='The python game',pos=(0,0), color=back):
        self.groups = allgroup, textgroup
        self.pos = pos
        self._layer =1
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.newMsg(msg,color)
    def update(self,time):
        pass
    def newMsg(self,msg, color=black):
        self.image = write(msg,color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos


def elastic_collision(sprite1, sprite2):
    """elasitc collision between 2 sprites (calculated as disc's).
       The function alters the dx and dy movement vectors of both sprites.
       The sprites need the property .mass, .radius, .pos[0], .pos[1], .dx, dy
       pos[0] is the x postion, pos[1] the y position"""
    # here we do some physics: the elastic
    # collision
    #
    # first we get the direction of the push.
    # Let's assume that the sprites are disk
    # shaped, so the direction of the force is
    # the direction of the distance.
    #dirx = sprite1.pos[0] - sprite2.pos[0]
    #diry = sprite1.pos[1] - sprite2.pos[1]
    dirx = sprite1.rect.centerx - sprite2.rect.centerx
    diry = sprite1.rect.centery - sprite2.rect.centery
    #
    # the velocity of the centre of mass
    sumofmasses = sprite1.mass + sprite2.mass
    sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
    sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
    # if we sutract the velocity of the centre
    # of mass from the velocity of the sprite,
    # we get it's velocity relative to the
    # centre of mass. And relative to the
    # centre of mass, it looks just like the
    # sprite is hitting a mirror.
    #
    bdxs = sprite2.dx - sx
    bdys = sprite2.dy - sy
    cbdxs = sprite1.dx - sx
    cbdys = sprite1.dy - sy
    # (dirx,diry) is perpendicular to the mirror
    # surface. We use the dot product to
    # project to that direction.
    distancesquare = dirx * dirx + diry * diry
    if distancesquare == 0:
        # no distance? this should not happen,
        # but just in case, we choose a random
        # direction
        dirx = random.randint(0,11) - 5.5
        diry = random.randint(0,11) - 5.5
        distancesquare = dirx * dirx + diry * diry
    dp = (bdxs * dirx + bdys * diry) # scalar product
    dp /= distancesquare # divide by distance * distance.
    cdp = (cbdxs * dirx + cbdys * diry)
    cdp /= distancesquare
    # We are done. (dirx * dp, diry * dp) is
    # the projection of the velocity
    # perpendicular to the virtual mirror
    # surface. Subtract it twice to get the
    # new direction.
    #
    # Only collide if the sprites are moving
    # towards each other: dp > 0
    if dp > 0:
        sprite2.dx -= 2 * dirx * dp 
        sprite2.dy -= 2 * diry * dp
        sprite1.dx -= 2 * dirx * cdp 
        sprite1.dy -= 2 * diry * cdp


def elasticCollision(sprite1,sprite2):
    #dirx = sprite1.pos[0] - sprite2.pos[0]
    #diry = sprite1.pos[1] - sprite2.pos[1]
    dirx = sprite1.rect.centerx - sprite2.rect.centerx
    diry = sprite1.rect.centery - sprite2.rect.centery

    sumofmasses = sprite1.mass + sprite2.mass
    sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
    sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
    # if we sutract the velocity of the centre
    bdxs = sprite2.dx - sx
    bdys = sprite2.dy - sy
    cbdxs = sprite1.dx - sx
    cbdys = sprite1.dy - sy

    distancesquare = dirx * dirx + diry * diry
    if distancesquare == 0:
        dirx = random.randint(0,11) - 5.5
        diry = random.randint(0,11) - 5.5
        distancesquare = dirx * dirx + diry * diry

    dp = (bdxs * dirx + bdys * diry) # scalar product
    dp /= distancesquare # divide by distance * distance.
    cdp = (cbdxs * dirx + cbdys * diry)
    cdp /= distancesquare
    # towards each other: dp > 0
    if dp > 0:
        sprite2.dx -= 2 * dirx * dp 
        sprite2.dy -= 2 * diry * dp
        sprite1.dx -= 2 * dirx * cdp 
        sprite1.dy -= 2 * diry * cdp
