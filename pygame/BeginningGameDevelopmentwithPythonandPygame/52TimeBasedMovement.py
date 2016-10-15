# Listing 5-2. Time-Based Movement
import pygame
from pygame.locals import *
from sys import exit

# constants
screensize = screenwidth,screenheight = 640,480
bgimage = 'sushiplate.jpg'
spriteimage = 'fugu.png'
black = pygame.Color('black')
green = pygame.Color('green')
blue = pygame.Color('blue')
white = pygame.Color('white')
 
# initialize pygame 
pygame.init()
screen = pygame.display.set_mode(screensize,0,32)
bgsurf = pygame.image.load(bgimage).convert()
spritesurf = pygame.image.load(spriteimage).convert_alpha()
# clock object
clock = pygame.time.Clock()

def getText(msg,color=blue):
    font = pygame.font.SysFont('bitstreamveraserif',20)
    textsurf = font.render(msg,True,color) # font.render(text,antialias,fg,bg)
    return textsurf

# X coordinate of our sprite
x = 0
# Speed in pixels per seconds
speedX = 100 # 250 

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()
    screen.blit(bgsurf,(0,0))
    screen.blit(spritesurf, (x,100) )

    # time passed(milliseconds) = clock.tick()
    timepassed = clock.tick(60)/1000.0
    dx = timepassed * speedX
    x += dx
    # time passed , distance moved, x coordinate
    timesurf    = getText(str(timepassed))
    distsurf    = getText(str(dx),green)
    xcoordsurf  = getText(str(x),black)
    msgX = 100
    msgY = screenheight - 40
    screen.blit(timesurf,(msgX,msgY))
    msgX += timesurf.get_width() + 40
    screen.blit(distsurf,(msgX,msgY))
    msgX += distsurf.get_width() + 40
    screen.blit(xcoordsurf,(msgX,msgY))
    print timepassed, dx, x
    # if image goes off the end of the screen, move it back
    if x > screen.get_width():
        x -= screenwidth
    pygame.display.update()

