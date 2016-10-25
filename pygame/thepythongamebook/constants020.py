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

def toRadian(degree):
    return degree * 2*pi/360

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
