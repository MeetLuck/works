import pygame,random,os
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
screensize = screenwidth,screenheight = 640,480
screen = pygame.display.set_mode( screensize )
clock = pygame.time.Clock()
fps = 60
# game constants
BIRDSPEEDMAX = 200
BIRDSPEEDMIN = 20
FRICTION = 0.99
#HITPOINTS = 100.0
# See http://en.wikipedia.org/wiki/Gravitational_acceleration
FORCEOFGRAVITY = 9.81 # in pixel per seconds
print pygame.ver

# colors
white   = pygame.Color('white')
red     = pygame.Color('red')
green   = pygame.Color('green')
blue    = pygame.Color('blue')
black   = pygame.Color('black')
yellow  = pygame.Color('yellow')
pink    = (200,0,255) # pink
randomblue = 0,0,random.randint(25,255)
randomred = random.randint(50,255),0,0
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

# check for Quit event
def checkQuit(): # event handler
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return False
        pygame.event.post(e)
    return True

