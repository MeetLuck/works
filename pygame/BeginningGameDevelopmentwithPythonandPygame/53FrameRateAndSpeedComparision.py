# Listing 5-3. Frame Rate and Speed Comparison
import pygame
from pygame.locals import *
from sys import exit

# constants
screensize = screenwidth,screenheight = 640,480
bgimage = 'sushiplate.jpg'
spriteimage = 'fugu.png'
black = pygame.Color('black')
white = pygame.Color('white')
red = pygame.Color('red')
green = pygame.Color('green')
blue = pygame.Color('blue')
 
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
x1 = 0.0
x2 = 0.0
fps = 60
# Speed in pixels per seconds
speedX = 50.0 # 250 
frameNo = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit(); exit()

    screen.blit(bgsurf,(0,0))
    screen.blit(spritesurf, (x1,50) )
    screen.blit(spritesurf, (x2,250) )

    # time passed(milliseconds) = clock.tick()
    timepassed = clock.tick(fps)/1000.0
    dx1 = round(timepassed * speedX,0)
    x1 += dx1

    if frameNo % 5 == 0:
        dx2 = timepassed * speedX
        x2 += 5.0 * dx2

    # time passed , distance moved, x coordinate
    timesurf    = getText(str(timepassed))
    distsurf    = getText(str(dx1),red)
    xcoordsurf  = getText(str(x1),black)
    msgX = 100
    msgY = screenheight - 40
    screen.blit(timesurf,(msgX,msgY))
    msgX += timesurf.get_width() + 40
    screen.blit(distsurf,(msgX,msgY))
    msgX += distsurf.get_width() + 40
    screen.blit(xcoordsurf,(msgX,msgY))
    print timepassed, str(dx1), dx2

    # if image goes off the end of the screen, move it back
    if x1 > screen.get_width():
        x1 -= screenwidth
    if x2 > screen.get_width():
        x2 -= screenwidth

    frameNo += 1
    pygame.display.update()

