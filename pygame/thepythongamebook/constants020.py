import pygame,random,os
from math import pi,sin,cos,atan,atan2
from colors import *
from vector import Vector
# game constants
#fps = 1
fps = 60
xtiles,ytiles = 30,20
folder = 'data'
GRAD = 2*pi/360
bgcolor = lightgray

# initialize pygame
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
screensize = screenwidth,screenheight = 640,480
screen = pygame.display.set_mode( screensize )
screenrect = screen.get_rect()
background = pygame.Surface((screen.get_size()))
background.fill(bgcolor) # fill grey light blue:(128,128,255) 

# KEYs for tank control
firekey     = (pygame.K_SPACE,pygame.K_DOWN)
MGfirekey   = (pygame.K_LCTRL, pygame.K_KP_ENTER)
turretLeftkey  = (pygame.K_w, pygame.K_LEFT)
turretRightkey = (pygame.K_s, pygame.K_RIGHT)
forwardkey      = (pygame.K_k, pygame.K_KP8)
backwardkey     = (pygame.K_j, pygame.K_KP5)
tankLeftkey     = (pygame.K_a, pygame.K_KP4)
tankRightkey    = (pygame.K_d, pygame.K_KP6)
#TankKeys = [firekey,MGfirekey,turrectLeft,turretRightkey,forwardkey,backwardkey,tankLeftkey,tankRightkey]

# paint a grid of white lines
for x in range(0,screenwidth,screenwidth/xtiles): #start, stop, step
    pygame.draw.line(background,gray, (x,0), (x,screenheight))
for y in range(0,screenheight,screenheight/ytiles): #start, stop, step
    pygame.draw.line(background,gray, (0,y), (screenwidth,y))
# paint upper rectangle to have background for text
pygame.draw.rect(background,lightgray, (0,0,screenwidth, 70))

background = background.convert()
screen.blit(background, (0,0)) # delete all
clock = pygame.time.Clock()    # create pygame clock object

# ---------- load sound -----------
cannonsound = pygame.mixer.Sound(os.path.join(folder,'cannon.ogg'))
mg1sound = pygame.mixer.Sound(os.path.join(folder,'mg1.ogg'))
mg2sound = pygame.mixer.Sound(os.path.join(folder,'mg2.ogg'))
mg3sound = pygame.mixer.Sound(os.path.join(folder,'mg3.ogg'))
#hitsound = pygame.mixer.Sound(os.path.join(folder,'beep.ogg'))

# game constants
BIRDSPEEDMAX = 200
FRAGMENTMAXSPEED = 200
FRICTION = 0.999
FORCEOFGRAVITY = 2.81 # in pixel per seconds

def drawTank(width,height):
    w,h = width,height
    image = pygame.Surface( (w,h) )
    image.fill(gray)
    color1 = (90,90,90)
    # tank decoration
    rect = image.get_rect()
    bodyrect  = (rect.left+5,rect.top+5),(w-10,h-10)
    leftrect  = rect.topleft,(w/6,h)
    rightrect = (rect.right-w/6,rect.top), (w,h)
    MGrect = pygame.Rect( (5+w/6,10),(15,7) )
    MGcenter = rect.centerx - MGrect.centerx, rect.centery - MGrect.centery 
    center = (w/2,h/2)
    r = w/3
    # draw body
    color0 = gray
    pygame.draw.rect(image,color0,bodyrect) # tank body, margin 5
    # draw leftside
    pygame.draw.rect(image,color1,leftrect) # tank left
    # draw rightside
    pygame.draw.rect(image,color1,rightrect) # right track
    # draw Machine Gun
    pygame.draw.rect(image,red,MGrect) # red bow rect left
    # draw rec Circle for turret
    pygame.draw.circle(image,red,center,r,2) # red circle for turret
    #image = pygame.transform.rotate(image,-90) # rotate so as to look EAST
    return image,MGcenter

def draw_cannon(boss, offset):
     # painting facing right, offset is the recoil
     width,height = 2*boss.width,2*boss.height
     image = pygame.Surface((width,height)) # created on the fly
     rect = image.get_rect()
     image.fill((gray)) # fill grey
     image.set_colorkey(gray)
     #pygame.draw.rect(image, green,  (1,1,width-2,height-2),1)
     pygame.draw.circle(image, red,   rect.center, 22) # red circle
     pygame.draw.circle(image, green, rect.center, 18) # green circle
     # turrect MG rectangle
     pygame.draw.rect(image, blue, (rect.centerx-10,rect.centery+10,25,4) ) # (width/2-10,height/2+10, 15,2))
     # green cannon
     h = 12
     cannonrect = rect.centerx-20-offset,rect.centery-h/2, width/2-offset,h
     pygame.draw.rect(image,green,cannonrect)
     # red rect
     pygame.draw.rect(image,red,cannonrect,2)
     #(width-20-offset,height-5, width-offset,10),1)
     return image

def toRadian(degree):
    return degree * 2*pi/360
 
def pressedKeysString():
    """returns the pressed keys (for the player1 tank) to be displayd in the status line"""
    pressedkeys = pygame.key.get_pressed()
    line = ""
    if pressedkeys[pygame.K_a]: line += "a "
    if pressedkeys[pygame.K_d]: line += "d "
    if pressedkeys[pygame.K_j]: line += "j "
    if pressedkeys[pygame.K_k]: line += "k "
    if pressedkeys[pygame.K_LCTRL]: line += "LCTRL"
    if pressedkeys[pygame.K_SPACE]: line += "SPACE"
    return line
def write(msg='pygame is cool',color=black):
    font = pygame.font.SysFont('Arial',20)
    textsurf = font.render(msg,True,color)
    textsurf = textsurf.convert_alpha()
    return textsurf
def getClassName(classinstance):
    # this function extract the class name of a instance of the class
    text = str(classinstance.__class__) # like <class '__main__.XWing'>
    parts = text.split('.') # [ <class '__main__, XWing'> ]
    return parts[-1][0:-2]  # take all except the last 2 charactors('>)
class Text(pygame.sprite.Sprite):
    number = 0
    book = {}
    def __init__(self,pos,msg):
        self.number = Text.number
        Text.number += 1
        Text.book[self.number] = self
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = Vector(pos)
        self.newMsg(msg)
    def update(self,seconds):
        pass
    def newMsg(self,msg, color=black):
        self.msg = msg
        self.image = write(msg,color)
        self.rect = self.image.get_rect()
        self.rect.center = tuple(self.pos)
