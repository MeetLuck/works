import pygame,random,os
from math import pi,sin,cos,atan2
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
screensize = screenwidth,screenheight = 640,480
screen = pygame.display.set_mode( screensize )
screenrect = screen.get_rect()
clock = pygame.time.Clock()
fps = 60

# game constants
BIRDSPEEDMAX = 200
FRAGMENTMAXSPEED = 200
FRICTION = 0.99
FORCEOFGRAVITY = 9.81 # in pixel per seconds
GRAD = 2*pi/360

# colors
white   = pygame.Color('white')
red     = pygame.Color('red')
green   = pygame.Color('green')
blue    = pygame.Color('blue')
black   = pygame.Color('black')
yellow  = pygame.Color('yellow')
pink    = (200,0,255) # pink
pink1   = 200,0,200
randomblue = 0,0,random.randint(25,255)
randomred = random.randint(50,255),0,0
randomdark = random.randint(1,50), random.randint(1,50), random.randint(1,50)
color02 = (66,1,166)
color1  = red
color2  = (0,255,155)
color3  = (100,55,155)
color4  = (250,100,255)
color5  = color4

def write(msg='pygame is cool'):
    font = pygame.font.SysFont('None',32)
    textsurf = font.render(msg,True,black)
    textsurf = textsurf.convert_alpha()
    return textsurf
def getClassName(classinstance):
    # this function extract the class name of a instance of the class
    text = str(classinstance.__class__) # like <class '__main__.XWing'>
    parts = text.split('.') # [ <class '__main__, XWing'> ]
    return parts[-1][0:-2]  # take all except the last 2 charactors('>)

# check for Quit event
def checkQuit(): # event handler
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return False
        pygame.event.post(e)
    return True
